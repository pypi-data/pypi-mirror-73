# -*- coding: utf-8 -*-
"""BITSdb Update class file."""

import json
import logging

from google.cloud import storage

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class Update(object):
    """BITSDB Update class."""

    def __init__(self, bitsdb, mri_bucket=None):
        """Initialize an Update class instance."""
        self.bitsdb = bitsdb
        self.mri_bucket = mri_bucket
        self.verbose = bitsdb.verbose

        self.auth = bitsdb.auth

        # collections
        self.cloud_collections = [
            'backupify_users',

            'github_collaborators',
            'github_members',
            'github_repos',
            'github_teams',
            'github_users',

            # 'google_billing_accounts',
            'google_calendars',
            'google_email_forwarding',
            # 'google_folders',
            'google_groups',
            'google_groups_by_member',
            'google_groups_settings',
            # 'google_organizations',
            'google_people',
            # 'google_projects',
            'google_resources',
            # 'google_service_accounts',
            'google_users',

            'pivotaltracker_projects',

            'scientific_calendars',

            'slack_channels',
            'slack_groups',
            'slack_usergroups',
            'slack_users',

            'workday_people',
        ]

        self.onprem_collections = [
            'ad_users',
            'ad_groups',

            'authorized_keys',

            'casper_computers',

            'ccure_credentials',
            'ccure_personnel',
            'ccure_personnel_types',

            'disclosure_people',
            'disclosure_users',

            'localmail_aliases',

            'nis_groups',
            'nis_mounts',
            'nis_users',

            'people',
            'people_users',

            'public_html',

            'space_buildings',
            'space_desks',
            'space_rooms',
            'space_seats',
            'space_users',

            'vendor_broad',
            'vendor_github',
            'vendor_google',
            'vendor_linkedin',
        ]

        self.collections = self.cloud_collections + self.onprem_collections

    #
    # Update functions
    #
    def add_missing_keys(self, data):
        """Add any missing keys to records for BigQuery."""
        # collect all keys used by any record
        allkeys = []
        for d in data:
            allkeys.extend(sorted(data[d]))
        keys = set(allkeys)
        # add missing keys to each record
        for d in data:
            e = data[d]
            for key in keys:
                if key not in e:
                    e[key] = None
        return data

    def get_collection(self, collection):
        """Return a collection for BITSdb."""
        function = 'get_%s' % (collection)
        if function not in dir(self):
            print('ERROR: Function not found: %s' % (function))
            return
        print('   Getting %s...' % (collection))

        try:
            return getattr(self, function)(self.bitsdb.auth)
        except Exception as e:
            print('ERROR: Failed to retrieve data for: {}'.format(collection))
            print(e)

    def save_to_gcs(self, path, data):
        """Save data to GCS as newline-deliminted JSON."""
        # create json string
        output = []
        for key in self.add_missing_keys(data):
            entry = data[key]
            output.append(json.dumps(entry, default=str))
        jsonstring = '\n'.join(output)

        storage_client = storage.Client()

        # set the bucket
        bucket = storage_client.bucket(self.mri_bucket)

        # create the blob
        blob = bucket.blob(path)

        # upload the blob
        print('   Updating {} in MRI BigQuery bucket...'.format(path.replace('.json', '')))
        try:
            blob.upload_from_string(jsonstring, content_type='application/json')
            return 'gs://{}/{}'.format(self.mri_bucket, path)
        except Exception as e:
            logging.error('Failed to upload to bucket!')
            logging.error(e)

    def update_collection(self, collection):
        """Update a collection."""
        print('Updating %s...' % (collection))
        data = self.get_collection(collection)
        if not isinstance(data, dict):
            logging.error('Data for collection "{}" is not an dict!'.format(collection))
            return
        print('   Found %s %s' % (len(data), collection))

        # only update if we have actual data
        if data:
            print('   Updating %s in MongoDB...' % (collection))
            m = self.auth.mongo()
            m.update_collection(collection, data, delete=True)

            # update mri bigquery data
            uri = self.update_mri_collection(collection, data)
            if uri:
                print('   Saved to GCS: {}'.format(uri))

    def update_mri_collection(self, collection, data):
        """Update the collection in the MRI BigQuery database."""
        exceptions = {
            'authorized_keys': 'accounts/authorized_keys',
            'people': 'people/people',
            'public_html': 'accounts/public_html',
            'vendor_broad': 'people/vendor_broad',
            'vendor_github': 'people/vendor_github',
            'vendor_google': 'people/vendor_google',
            'vendor_linkedin': 'people/vendor_linkedin',
        }
        path = collection.replace('_', '/', 1)
        if collection in exceptions:
            path = exceptions[collection]
        path = '{}.json'.format(path)
        return self.save_to_gcs(path, data)

    #
    # Wrapper functions
    #
    def update_all(self):
        """Update all Collections."""
        self.update_cloud_collections()
        print()
        self.update_onprem_collections()

    def update_collections(self, collections):
        """Update given Collections."""
        for collection in collections:
            try:
                self.update_collection(collection)
            except Exception as e:
                logging.error('Failed updating collection: {}'.format(collection))
                logging.error(e)

    def update_cloud_collections(self):
        """Update Collections sourced from cloud services."""
        print('===== Cloud Collections =====\n')
        self.update_collections(self.cloud_collections)

    def update_onprem_collections(self):
        """Update Collections sourced from on-prem services."""
        print('===== On-Prem Collections =====\n')
        self.update_collections(self.onprem_collections)

    #
    # Functions for getting data from cloud sources
    #

    # backupify
    def get_backupify_users(self, auth):
        """Return a dict of Backupify Users for BITSdb."""
        b = auth.backupify()
        return b.get_users_dict()

    # pivotaltracker
    def get_pivotaltracker_projects(self, auth):
        """Return a dict or Pivotal Tracker Projects for BITSdb."""
        p = auth.pivotaltracker()
        return p.get_projects()

    # github
    def get_github_collaborators(self, auth):
        """Return a dict or GitHub Org Collaborators for BITSdb."""
        g = auth.github()
        return g.get_org_outside_collaborators_dict()

    def get_github_members(self, auth):
        """Return a dict or GitHub Org Members for BITSdb."""
        g = auth.github()
        return g.get_org_members_dict()

    def get_github_repos(self, auth):
        """Return a dict or GitHub Org Repos for BITSdb."""
        g = auth.github()
        return g.get_org_repos_dict()

    def get_github_teams(self, auth):
        """Return a dict or GitHub Org Teams for BITSdb."""
        g = auth.github()
        return g.get_org_teams_dict()

    def get_github_users(self, auth):
        """Return a dict or GitHub Users for BITSdb."""
        g = auth.github()
        users = {}
        for user in g.update().update_users():
            user_id = user['id']
            users[user_id] = user
        return users

    # Google
    def get_google_billing_accounts(self, auth):
        """Return a dict of Google Billing Accounts for BITSdb."""
        g = auth.google()
        return g.getBillingAccounts(projects=True, iampolicy=True)

    def get_google_calendars(self, auth):
        """Return a dict of Google Calendars for BITSdb."""
        g = auth.google()
        return g.getAllCalendars()

    def get_google_folders(self, auth):
        """Return a dict of Google Org Folders for BITSdb."""
        g = auth.google()
        g.auth_service_account(g.scopes, g.subject)
        return g.crm().get_organizations_folders()

    def get_google_email_forwarding(self, auth):
        """Return a dict of Google Email Forwarding for BITSdb."""
        g = auth.google()
        return g.getEmailForwardingSettings()

    def get_google_groups(self, auth):
        """Return a dict of Google Groups for BITSdb."""
        g = auth.google()
        g.auth_service_account(g.scopes, g.subject)
        return g.directory().get_groups_dict()

    def get_google_groups_by_member(self, auth):
        """Return a dict of Google Groups by Member for BITSdb."""
        b = auth.mongo()
        g = auth.google()
        bitsdb_users = b.getCollection('google_users')
        bitsdb_groups = b.getCollection('google_groups_with_members')
        return g.getGroupsByMember(
            bitsdb_groups,
            bitsdb_users,
        )

    def get_google_groups_settings(self, auth):
        """Return a dict of Google Groups Settings for BITSdb."""
        g = auth.google()
        return g.getAllGroupsSettings()

    def get_google_organizations(self, auth):
        """Return a dict of Google Organizations for BITSdb."""
        g = auth.google()
        g.auth_service_account(g.scopes, g.subject)
        return g.crm().get_organizations_iampolicy()

    def get_google_people(self, auth):
        """Return a dict of Google People for BITSdb."""
        g = auth.google()
        return g.getPeople()

    def get_google_projects(self, auth):
        """Return a dict of Google Projects for BITSdb."""
        g = auth.google()
        return g.getProjects()

    def get_google_resources(self, auth):
        """Return a dict of Google Resources for BITSdb."""
        g = auth.google()
        g.auth_service_account(g.scopes, g.subject)
        return g.directory().get_resource_calendars_dict()

    def get_google_service_accounts(self, auth):
        """Return a dict of Google Service Accounts for BITSdb."""
        g = auth.google()
        return g.getAllServiceAccounts()

    def get_google_users(self, auth):
        """Return a dict of Google Users for BITSdb."""
        g = auth.google()
        return g.getUsers()

    # localmail
    def get_localmail_aliases(self, auth):
        """Return a dict of Localmail aliases for BITSdb."""
        lm = auth.localmail()
        return lm.get_localmail_aliases()

    # scientific calendars
    def get_scientific_calendars(self, auth):
        """Return a dict of Scientific Calendars for BITSdb."""
        c = auth.calendar()
        return c.getScientificCalendars()

    # slack
    def get_slack_channels(self, auth):
        """Return a dict or Slack Channels for BITSdb."""
        s = auth.slack()
        return s.get_channels_dict()

    def get_slack_groups(self, auth):
        """Return a dict or Slack Groups for BITSdb."""
        s = auth.slack()
        return s.get_groups_dict()

    def get_slack_usergroups(self, auth):
        """Return a dict or Slack Usergroups for BITSdb."""
        s = auth.slack()
        return s.get_usergroups_dict(include_count=True)

    def get_slack_users(self, auth):
        """Return a dict or Slack Users for BITSdb."""
        s = auth.slack()
        return s.get_users_dict()

    # workday
    def get_workday_people(self, auth):
        """Return a dict or Workday People for BITSdb."""
        w = auth.workday()
        return w.find_dict()

    #
    # Functions for getting data from on-prem sources
    #

    # account info - unix
    def get_authorized_keys(self, auth):
        """Return a dict of SSH authorized keys for BITSdb."""
        a = auth.accounts()
        return a.getAuthorizedKeys()

    def get_public_html(self, auth):
        """Return a dict of public_html directories for BITSdb."""
        a = auth.accounts()
        return a.getPublicHtml()

    # ad
    def get_ad_groups(self, auth):
        """Return a dict of AD groups for BITSdb."""
        ad = auth.ad()
        return ad.get_groups(bytes_mode=False)

    def get_ad_users(self, auth):
        """Return a dict of AD users for BITSdb."""
        ad = auth.ad()
        return ad.get_users(bytes_mode=False)

    # casper
    def get_casper_computers(self, auth):
        """Return a dict of Casper (JAMF) computers for BITSdb."""
        c = auth.casper()
        return c.getComputers()

    # ccure
    def get_ccure_credentials(self, auth):
        """Return a dict of ccure cards (credentials) for BITSdb."""
        c = auth.ccure()
        return c.getCredentials()

    def get_ccure_personnel(self, auth):
        """Return a dict of ccure people (personnel) for BITSdb."""
        c = auth.ccure()
        return c.getPersonnel()

    def get_ccure_personnel_types(self, auth):
        """Return a dict of ccure personnel types for BITSdb."""
        c = auth.ccure()
        return c.getPersonnelTypes()

    # disclosure
    def get_disclosure_people(self, auth):
        """Return a dict of disclosure people for BITSdb."""
        d = auth.disclosure()
        mongo_people = d.getPeople()
        people = {}
        for key in mongo_people:
            p = mongo_people[key]
            key = p['pid']
            del p['_id']
            people[key] = p
        return people

    def get_disclosure_users(self, auth):
        """Return a dict of disclosure users for BITSdb."""
        d = auth.disclosure()
        mongo_users = d.getUsers()
        users = {}
        for key in mongo_users:
            p = mongo_users[key]
            key = p['email']
            del p['_id']
            users[key] = p
        return users

    # nis
    def get_nis_groups(self, auth):
        """Return a dict of NIS groups (group) for BITSdb."""
        n = auth.nis()
        return n.getGroups()

    def get_nis_mounts(self, auth):
        """Return a dict of NIS mounts (mounts.byname) for BITSdb."""
        n = auth.nis()
        return n.getMounts()

    def get_nis_users(self, auth):
        """Return a dict of NIS users (passwd) for BITSdb."""
        n = auth.nis()
        return n.getPasswd()

    # people
    def get_people(self, auth):
        """Return a dict of People for BITSdb."""
        p = auth.people()
        return p.getPeople()

    def get_people_users(self, auth):
        """Return a dict of People users for BITSdb."""
        p = auth.people()
        return p.getUsers()

    def get_vendor_broad(self, auth):
        """Return a dict of People broad vendor data for BITSdb."""
        p = auth.people()
        return p.getVendorData('broad')

    def get_vendor_github(self, auth):
        """Return a dict of People github vendor data for BITSdb."""
        p = auth.people()
        return p.getVendorData('github')

    def get_vendor_google(self, auth):
        """Return a dict of People google vendor data for BITSdb."""
        p = auth.people()
        return p.getVendorData('google')

    def get_vendor_linkedin(self, auth):
        """Return a dict of People linkedin vendor data for BITSdb."""
        p = auth.people()
        return p.getVendorData('linkedin')

    # space
    def get_space_buildings(self, auth):
        """Return a dict of Space buildings for BITSdb."""
        s = auth.space()
        return s.getBuildings()

    def get_space_desks(self, auth):
        """Return a dict of Space desks for BITSdb."""
        s = auth.space()
        return s.getDesks()

    def get_space_rooms(self, auth):
        """Return a dict of Space rooms for BITSdb."""
        s = auth.space()
        return s.getRooms()

    def get_space_seats(self, auth):
        """Return a dict of Space seats for BITSdb."""
        s = auth.space()
        return s.getSeats()

    def get_space_users(self, auth):
        """Return a dict of Space users for BITSdb."""
        s = auth.space()
        return s.getUsers()
