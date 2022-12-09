# a solid chunk of the code below was adapted from 
# https://github.com/alfonsof/google-cloud-python-examples/blob/master/gcloudcomputeengine/computeenginehelper.py

import googleapiclient.discovery

# ZONE_NAME           = 'us-east1-b'                      # Zone name
# PROJECT_NAME        = 'gcloud-java-examples'            # Project name
# IMAGE_NAME          = "ubuntu-1604-lts"                 # Image name
# IMAGE_PROJECT_NAME  = "ubuntu-os-cloud"                 # Image project name
# INSTANCE_TYPE       = "n1-standard-1"                   # Instance type
# INSTANCE_NAME       = "my-instance"                     # Name of the instance

class ComputeEngine:

    def __init__(self, project, zone, image_family=None, image_project=None, instance_type=None, instance_name=None):

        self.project = project
        self.zone = zone
        self.image_family = image_family
        self.image_project = image_project
        self.instance_type = instance_type
        self.instance_name = instance_name

    def list_instances(self):
        """
        List all Compute Engine VM instances associated with an Google Cloud account
        """
        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        print('Listing VM instances ...')

        # Describe instances
        response = compute.instances().list(project=self.project, zone=self.zone).execute()
        # TODO: test this and see if it's a dictionary that can be easily manipulated for display or an iterable

        print('Instances in project "%s" and zone "%s":' % (self.project, self.zone))
        if (response.get('items')):
            for instance in response['items']:
                print(' - Id:           ' + instance['id'])
                print('   Name:         ' + instance['name'])
                print('   Status:       ' + instance['status'])
                print('   Machine type: ' + instance['machineType'])
        else:
            print('NO instances')

        return


    def _create_instance(self, **kwargs):
        """
        Create a Compute Engine VM instance
        """
        # TODO: possibly not support this in streamlit? it seems like giving the user too much power!
        image_project = kwargs.pop('image_project', self.image_project)
        image_family = kwargs.pop('image_family', self.image_family)
        instance_type = kwargs.pop('instance_type', self.instance_type)
        instance_name = kwargs.pop('instance_name', self.instance_name)

        if image_project is None:
            raise ValueError('image_project_name is None. Please specify a value when calling this method.')
        if image_family is None:
            raise ValueError('image_name is None. Please specify a value when calling this method.')
        if instance_type is None:
            raise ValueError('instance_type is None. Please specify a value when calling this method.')
        if instance_name is None:
            raise ValueError('instance_name is None. Please specify a value when calling this method.')

        # override init values after an instance is created
        self.image_family = image_family
        self.image_project = image_project
        self.instance_type = instance_type
        self.instance_name = instance_name

        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        print('Creating VM instance ...')

        # Get the latest image
        image_response = compute.images().getFromFamily(
                                project=image_project, family=image_family).execute()
        source_disk_image = image_response['selfLink']

        # Configure the machine
        #machine_type = 'zones/' + ZONE_NAME + '/machineTypes/' + INSTANCE_TYPE
        machine_type = 'zones/%s/machineTypes/%s' % (self.zone, instance_type)

        config = {
            'name': instance_name,
            'machineType': machine_type,

            # Specify the boot disk and the image to use as a source.
            'disks': [
                {
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': source_disk_image,
                    }
                }
            ],

            # Specify a network interface with NAT to access the public
            # internet.
            'networkInterfaces': [{
                'network': 'global/networks/default',
                'accessConfigs': [
                    {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
                ]
            }],

            # Allow the instance to access cloud storage and logging.
            'serviceAccounts': [{
                'email': 'default',
                'scopes': [
                    'https://www.googleapis.com/auth/devstorage.read_write',
                    'https://www.googleapis.com/auth/logging.write'
                ]
            }]
        }

        response = compute.instances().insert(project=self.project,
                                zone=self.zone,
                                body=config).execute()

        print('Instance Id: ' + response['targetId'])

        return response['targetId']


    def list_instance(self, **kwargs):
        """
        List a Compute Engine VM instance
        """
        instance_name = kwargs.pop('instance_name', self.instance_name)
        if instance_name is None:
            raise ValueError('instance_name is None. Please specify a value when calling this method.')


        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        # print('Listing VM instance ...')
        # print('Instance Id: ' + instance_id)

        # List the VM instance
        response = compute.instances().get(project=self.project, zone=self.zone, instance=instance_name).execute()

        print(' - Id:           ' + response['id'])
        print('   Name:         ' + response['name'])
        print('   Status:       ' + response['status'])
        print('   Machine type: ' + response['machineType'])

        return


    def start_instance(self, **kwargs):
        """
        Start a Compute Engine VM instance
        """
        instance_name = kwargs.pop('instance_name', self.instance_name)
        if instance_name is None:
            raise ValueError('instance_name is None. Please specify a value when calling this method.')

        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        # print('Starting VM instance ...')
        # print('Instance Id: ' + instance_id)

        # Start VM instance
        compute.instances().start(
            project=self.project,
            zone=self.zone,
            instance=instance_name).execute()

        return


    def stop_instance(self, **kwargs):
        """
        Stop a Compute Engine VM instance
        """
        instance_name = kwargs.pop('instance_name', self.instance_name)
        if instance_name is None:
            raise ValueError('instance_name is None. Please specify a value when calling this method.')

        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        # print('Stopping VM instance ...')
        # print('Instance Id: ' + instance_id)

        # Stop VM instance
        compute.instances().stop(
            project=self.project,
            zone=self.zone,
            instance=instance_name).execute()

        return


    def reset_instance(self, **kwargs):
        """
        Reset a Compute Engine VM instance
        """
        instance_name = kwargs.pop('instance_name', self.instance_name)
        if instance_name is None:
            raise ValueError('instance_name is None. Please specify a value when calling this method.')

        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        # print('Resetting VM instance ...')
        # print('Instance Id: ' + instance_id)

        # Reset VM instance
        compute.instances().reset(
            project=self.project,
            zone=self.zone,
            instance=instance_name).execute()

        return


    def _delete_instance(self, **kwargs):
        """
        Delete a Compute Engine VM instance
        """
        instance_name = kwargs.pop('instance_name', self.instance_name)
        if instance_name is None:
            raise ValueError('instance_name is None. Please specify a value when calling this method.')

        # Build and initialize the API
        compute = googleapiclient.discovery.build('compute', 'v1')

        # print('Deleting VM instance ...')
        # print('Instance Id: ' + instance_id)

        # Delete VM instance
        compute.instances().delete(
            project=self.project,
            zone=self.zone,
            instance=instance_name).execute()

        return