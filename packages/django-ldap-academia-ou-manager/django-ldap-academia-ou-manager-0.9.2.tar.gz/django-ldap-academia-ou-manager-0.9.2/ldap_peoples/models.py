import ldap
import ldapdb.models
import logging
import os

from django.conf import settings
from django.db import connections
from django.db.models import fields
from django.utils import timezone

from django.db import models
from django.utils.translation import gettext as _
from ldapdb.models.fields import (CharField,
                                  DateTimeField,
                                  ImageField,
                                  IntegerField,
                                  TimestampField)
from pySSHA import ssha
from .hash_functions import encode_secret
from . ldap_utils import (parse_generalized_time,
                          parse_pwdfailure_time,
                          get_expiration_date,
                          format_generalized_time)
from . model_fields import (TimeStampField,
                            DateField,
                            MultiValueField,
                            ListField,
                            EmailListField,
                            SchacPersonalUniqueIdListField,
                            SchacPersonalUniqueCodeListField,
                            ScopedListField,
                            eduPersonAffiliationListField,
                            eduPersonScopedAffiliationListField,
                            SchacHomeOrganizationTypeListField,
                            TitleField)
from . serializers import LdapSerializer


logger = logging.getLogger(__name__)


class LdapGroup(ldapdb.models.Model):
    """
    Class for representing an LDAP group entry.
    This is a memberOf bind
    http://www.openldap.org/software/man.cgi?query=slapo-memberof&sektion=5&apropos=0&manpath=OpenLDAP+2.4-Release
    """
    # LDAP meta-data
    base_dn = "ou=groups,{}".format(settings.LDAP_BASEDN)
    object_classes = ['groupOfNames',]

    cn = CharField(db_column='cn',
                   primary_key=True)
    member = ListField(db_column='member', default=[])


    class Meta:
        verbose_name = _('LDAP MemberOf Group')
        verbose_name_plural = _('LDAP MemberOf Groups')

    def add_member(self, member_dn_obj):
        members = self.member.split(os.linesep)
        if not member_dn_obj in members:
            members.append(member_dn_obj.dn.strip())
        self.member = os.linesep.join(members)
        self.save()

    def remove_member(self, member_dn_obj):
        members = self.member.split(os.linesep)
        if member_dn_obj.dn in members:
            members = [i for i in members if i != member_dn_obj.dn ]
        self.member = os.linesep.join(members)
        self.save()

    def __str__(self):
        return self.cn


class LdapAcademiaUser(ldapdb.models.Model, LdapSerializer):
    """
    Class for representing an LDAP user entry.
    """
    # LDAP meta-data
    base_dn = "{}".format(settings.LDAP_PEOPLE_DN)

    object_classes = ['inetOrgPerson',
                      'organizationalPerson',
                      'person',
                      # WARNING: only who have these OC will be filtered
                      'userSecurityInformation',
                      'eduPerson',
                      'radiusprofile',
                      'sambaSamAccount',
                      'schacContactLocation',
                      'schacEmployeeInfo',
                      'schacEntryConfidentiality',
                      'schacEntryMetadata',
                      'schacExperimentalOC',
                      'schacGroupMembership',
                      'schacLinkageIdentifiers',
                      'schacPersonalCharacteristics',
                      'schacUserEntitlements']

    # inetOrgPerson
    uid = CharField(db_column='uid',
                    verbose_name="User ID",
                    help_text="uid",
                    primary_key=True)
    cn = CharField(db_column='cn',
                     verbose_name=_("Common Name"),
                     help_text='cn',
                     blank=False)
    givenName = CharField(db_column='givenName',
                          help_text="givenName",
                          verbose_name=_("First Name"),
                          blank=True, null=True)
    sn = CharField("Last name", db_column='sn',
                   help_text='sn',
                   blank=False)
    displayName = CharField(db_column='displayName',
                            help_text='displayName',
                            blank=True, null=True)
    title = TitleField(db_column='title',
                       help_text='title',
                       blank=True, null=True)
    telephoneNumber = ListField(db_column='telephoneNumber',
                                blank=True)
    mail = EmailListField(db_column='mail',
                          default='',
                          blank=True, null=True)
    userPassword = CharField(db_column='userPassword',
                             verbose_name="LDAP Password",
                             blank=True, null=True)
                             # editable=False)
    sambaNTPassword = CharField(db_column='sambaNTPassword',
                                help_text=_("SAMBA NT Password (freeRadius PEAP)"),
                                blank=True, null=True,)
    sambaSID = CharField(db_column='sambaSID',
                                help_text=_("Microsoft Network unique identificator"),
                                blank=True, null=True)
    # academia
    eduPersonPrincipalName = CharField(db_column='eduPersonPrincipalName',
                                       help_text=_("A scoped identifier for a person"),
                                       verbose_name='ePPN, Eduperson PrincipalName',
                                       blank=True, null=True)
    eduPersonAffiliation = eduPersonAffiliationListField(db_column='eduPersonAffiliation',
                                     help_text=_("Membership and "
                                                 "affiliation organization"),
                                     verbose_name='Eduperson Affiliation',
                                     blank=True, null=True)
    eduPersonScopedAffiliation = eduPersonScopedAffiliationListField(db_column='eduPersonScopedAffiliation',
                                                 help_text=_("Membership and scoped"
                                                             "affiliation organization."
                                                             "Es: affliation@istitution"),
                                                 verbose_name='ScopedAffiliation',
                                                 blank=True, null=True)
    eduPersonEntitlement = ListField(db_column='eduPersonEntitlement',
                                     help_text=("eduPersonEntitlement"),
                                     verbose_name='eduPersonEntitlement',
                                     #default=settings.DEFAULT_EDUPERSON_ENTITLEMENT,
                                     blank=True, null=True)
    eduPersonOrcid = CharField(db_column='eduPersonOrcid',
                               verbose_name='EduPerson Orcid',
                               help_text=_("ORCID user identifier released and managed by orcid.org"),
                               blank=True, null=True)
    eduPersonAssurance = CharField(db_column='eduPersonAssurance',
                                   verbose_name='EduPerson Assurance',
                                   choices = settings.EDUPERSON_ASSURANCES,
                                   default = settings.EDUPERSON_DEFAULT_ASSURANCE,
                                   help_text=_("Identity proofing and credential issuance (LoA)"),
                                   blank=True, null=True)
    # SCHAC 2015
    schacHomeOrganization = CharField(db_column='schacHomeOrganization',
                                      help_text=_(("The persons home organization "
                                                   "using the domain of the organization.")),
                                      #  default=settings.SCHAC_HOMEORGANIZATION_DEFAULT,
                                      verbose_name='schacHomeOrganization',
                                      blank=True, null=True)
    schacHomeOrganizationType = SchacHomeOrganizationTypeListField(db_column='schacHomeOrganizationType',
                                             help_text=_("Type of a Home Organization"),
                                             blank=True, null=True)
    schacPersonalUniqueID = SchacPersonalUniqueIdListField(db_column='schacPersonalUniqueID',
                                      verbose_name="schacPersonalUniqueID",
                                      help_text=_(("Unique Legal Identifier of "
                                                   "a person, es: codice fiscale")),
                                      blank=True, null=True, )
    schacPersonalUniqueCode = SchacPersonalUniqueCodeListField(db_column='schacPersonalUniqueCode',
                                  verbose_name="schacPersonalUniqueCode",
                                  help_text=_(('Specifies a "unique code" '
                                               'for the subject it is associated with')),
                                  blank=True, null=True)
    schacGender = CharField(db_column='schacGender', default='0',
                               choices=(('0', _('Not know')),
                                        ('1', _('Male')),
                                        ('2', _('Female')),
                                        ('9', _('Not specified'))),
                            help_text=_("OID: 1.3.6.1.4.1.25178.1.2.2"),
                            verbose_name='schacGender',
                            blank=True, null=True)
    schacDateOfBirth = DateField(db_column='schacDateOfBirth',
                                 format="%Y%m%d", # from_ldap format
                                 help_text=_("OID 1.3.6.1.4.1.1466.115.121.1.36"),
                                 verbose_name='schacDateOfBirth',
                                 blank=True, null=True)
    schacPlaceOfBirth = CharField(db_column='schacPlaceOfBirth',
                                  help_text=_("OID: 1.3.6.1.4.1.1466.115.121.1.15"),
                                  verbose_name='schacPlaceOfBirth',
                                  blank=True, null=True)
    schacExpiryDate = TimeStampField(db_column='schacExpiryDate',
                                     help_text=_(('Date from which the set of '
                                                  'data is to be considered invalid')),
                                     default=get_expiration_date,
                                     format=settings.DATETIME_FORMAT,
                                     blank=False, null=True)
    # readonly
    memberOf = MultiValueField(db_column='memberOf', editable=False, null=True)
    createTimestamp =  DateTimeField(db_column='createTimestamp', editable=False, null=True)
    modifyTimestamp =  DateTimeField(db_column='modifyTimestamp', editable=False, null=True)
    creatorsName = CharField(db_column='creatorsName', editable=False, null=True)
    modifiersName = CharField(db_column='modifiersName', editable=False, null=True)

    # If pwdAccountLockedTime is set to 000001010000Z, the user's account has been permanently locked and may only be unlocked by an administrator.
    # Note that account locking only takes effect when the pwdLockout password policy attribute is set to "TRUE".
    pwdAccountLockedTime = CharField(db_column='pwdAccountLockedTime')
    pwdFailureTime = MultiValueField(db_column='pwdFailureTime', editable=False)
    pwdChangedTime = TimeStampField(db_column='pwdChangedTime', editable=False)
    pwdHistory = ListField(db_column='pwdHistory', editable=False)

    class Meta:
        verbose_name = _('LDAP Academia User')
        verbose_name_plural = _('LDAP Academia Users')

    def distinguished_name(self):
        return 'uid={},{}'.format(self.uid, self.base_dn)

    def is_active(self):
        if self.pwdAccountLockedTime: return False
        if self.schacExpiryDate:
            if self.schacExpiryDate < timezone.localtime(): return False
        return True

    def is_renewable(self):
        return self.pwdAccountLockedTime != settings.PPOLICY_PERMANENT_LOCKED_TIME

    def lock(self):
        self.pwdAccountLockedTime = settings.PPOLICY_PERMANENT_LOCKED_TIME
        self.save()
        logger.debug('Locked {} with {}'.format(self.uid, self.pwdAccountLockedTime))
        return self.pwdAccountLockedTime

    def disable(self):
        self.pwdAccountLockedTime = format_generalized_time(timezone.localtime())
        self.save()
        logger.debug('Disabled {} with {}'.format(self.uid, self.pwdAccountLockedTime))
        return self.pwdAccountLockedTime

    def enable(self):
        self.pwdAccountLockedTime = None
        self.save()
        logger.debug('Enabled {} with {}'.format(self.uid, 'pwdAccountLockedTime = None'))

    def locked_time(self):
        if self.pwdAccountLockedTime == settings.PPOLICY_PERMANENT_LOCKED_TIME:
            return '{}: locked by admin'.format(settings.PPOLICY_PERMANENT_LOCKED_TIME)
        elif self.pwdAccountLockedTime:
            return parse_generalized_time(self.pwdAccountLockedTime)

    def failure_times(self):
        if not self.pwdFailureTime: return
        times = self.pwdFailureTime.split(os.linesep)
        failures = [parse_pwdfailure_time(i).strftime(settings.DATETIME_FORMAT) for i in times]
        parsed =  os.linesep.join(failures)
        return parsed

    def set_schacPersonalUniqueID(self, value, save=False,
                                  doc_type=settings.SCHAC_PERSONALUNIQUEID_DEFAULT_DOCUMENT_CODE,
                                  country_code=settings.SCHAC_PERSONALUNIQUEID_DEFAULT_COUNTRYCODE):

        if settings.SCHAC_PERSONALUNIQUEID_DEFAULT_PREFIX not in value:
            unique_id = ':'.join((settings.SCHAC_PERSONALUNIQUEID_DEFAULT_PREFIX,
                                  country_code,
                                  doc_type, value))
        if self.schacPersonalUniqueID:
            if unique_id not in self.schacPersonalUniqueID:
                self.schacPersonalUniqueID.append(unique_id)
        else:
            self.schacPersonalUniqueID = [unique_id]
        if save:
            self.save()

    def set_default_schacHomeOrganization(self, save=False):
        if not self.schacHomeOrganization:
            self.schacHomeOrganization = settings.SCHAC_HOMEORGANIZATION_DEFAULT
        if save:
            self.save()

    def set_default_schacHomeOrganizationType(self, save=False,
                                      country_code=settings.SCHAC_PERSONALUNIQUEID_DEFAULT_COUNTRYCODE):
        if not self.schacHomeOrganization:
            logger.warn('Cannot set schacHomeOrganizationType without schacHomeOrganization')
            return
        if not self.schacHomeOrganizationType:
            self.schacHomeOrganizationType = settings.SCHAC_HOMEORGANIZATIONTYPE_DEFAULT
        if save:
            self.save()

    def set_default_eppn(self, save=False):
        if not self.schacHomeOrganization:
            logger.warn('Cannot set eduPersonPrincipalName without schacHomeOrganization')
            return
        self.eduPersonPrincipalName = '@'.join((self.uid, self.schacHomeOrganization))
        if save:
            self.save()
        return self.eduPersonPrincipalName

    def update_eduPersonScopedAffiliation(self, save=False):
        if not self.schacHomeOrganization:
            logger.warn('Cannot set ScopedAffiliations without schacHomeOrganization')
            return

        updated = [ele for ele in self.eduPersonScopedAffiliation]
        updated.extend(['@'.join((ele, self.schacHomeOrganization))
                        for ele in self.eduPersonAffiliation])
        updated = list(set(updated))
        if self.eduPersonScopedAffiliation != updated:
            self.eduPersonScopedAffiliation = updated
            if save:
                self.save()
        return self.eduPersonScopedAffiliation

    def membership(self):
        if self.memberOf: return self.memberOf
        # memberOf fill fields in people entries only if a change/write happens in its definitions
        try:
            membership = LdapGroup.objects.filter(member__contains=self.dn)
            if membership:
                # return os.linesep.join([m.dn for m in membership])
                return [i.cn for i in membership]
        except ldap.FILTER_ERROR as e:
            logger.warn('No membership found: {}'.format(e))
            return []

    def check_pwdHistory(self, password):
        """
        if returns True means that this password was already used in the past
        """
        res = None
        for e in self.pwdHistory:
            old_pwd = e.split('#')[-1]
            res = ssha.checkPassword(password,
                                     old_pwd,
                                     settings.LDAP_PASSWORD_SALT_SIZE,
                                     'suffixed')
            if res: break
        return res

    def set_password(self, password, old_password=None):
        ldap_conn = connections['ldap']
        ldap_conn.ensure_connection()
        ldap_conn.connection.passwd_s(user = self.dn,
                                      oldpw = old_password,
                                      newpw = password.encode(settings.FILE_CHARSET))
        ldap_conn.connection.unbind_s()
        self.refresh_from_db()
        logger.info('{} changed password'.format(self.uid))
        return True

    def set_password_custom(self, password, hashtype=settings.DEFAULT_SECRET_TYPE):
        """
        EXPERIMENTAL - do not use in production
        encode the password, this could not works on some LDAP servers
        """
        # password encoding
        if password:
            self.userPassword = encode_secret(hashtype, password)
        # additional password fields encoding
        enc_map = settings.PASSWD_FIELDS_MAP
        for field in enc_map:
            if not hasattr(self, field):
                continue
            enc_value = encode_secret(enc_map[field], password)
            setattr(self, field, enc_value)
        self.save()
        logger.info('{} changed password'.format(self.uid))
        return self.userPassword

    def set_default_schacExpiryDate(self, save=False):
        # set a default ExpiryDate if not available
        if self.pwdChangedTime:
            self.schacExpiryDate = self.pwdChangedTime + timezone.timedelta(days=settings.SHAC_EXPIRY_DURATION_DAYS)
        else:
            self.schacExpiryDate = timezone.localtime() + timezone.timedelta(days=settings.SHAC_EXPIRY_DURATION_DAYS)
        if save:
            self.save()
        logger.debug('{} set default schacExpiryDate'.format(self.uid))
        return self.schacExpiryDate

    #  def save(self, *args, **kwargs):
        #  """
        #  Just check and update eppn
        #  """
        #  if not self.eduPersonPrincipalName or \
           #  self.uid not in self.eduPersonPrincipalName:
            #  self.set_default_eppn()
        #  super().save(*args, **kwargs)

    def __str__(self):
        return self.dn
