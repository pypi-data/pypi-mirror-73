import json

from botocore.config import Config
from botocore.exceptions import ClientError
from hca_util.local_state import get_selected_area
from hca_util.common import print_err
from hca_util.command.area import CmdArea


class CmdDelete:
    """
    user: both wrangler and contributor, though contributor can't delete folder
    aws resource or client used in command - s3 resource (bucket.objects/ obj.delete)
    """

    def __init__(self, aws, args):
        self.aws = aws
        self.args = args

    def run(self):

        selected_area = get_selected_area()

        if not selected_area:
            print('No area selected')
            return

        try:
            s3_resource = self.aws.common_session.resource('s3', endpoint_url='https://s3.embassy.ebi.ac.uk/', config=Config(s3={'addressing_style': 'path'}))
            bucket = s3_resource.Bucket(self.aws.bucket_name)

            if self.args.d:  # delete area
                if self.aws.is_contributor:
                    print('You don\'t have permission to use this command')
                    return

                confirm = input(f'Confirm delete {selected_area}? Y/y to proceed: ')

                if confirm.lower() == 'y':
                    print('Deleting...')

                    for obj in bucket.objects.filter(Prefix=selected_area):
                        print(obj.key)
                        obj.delete()

                    # delete bucket policy for HCAContributer-folder permissions
                    # only wrangler who has perms to set policy can do this
                    delete_dir_perms_from_bucket_policy(s3_resource, self.aws.bucket_name, selected_area)

                    # clear selected area
                    CmdArea.clear(False)
                return

            if self.args.a:  # delete all files
                print('Deleting...')
                for obj in bucket.objects.filter(Prefix=selected_area):
                    # do not delete folder object
                    if obj.key == selected_area:
                        continue
                    print(obj.key)
                    obj.delete()
                return

            if self.args.f:  # delete list of file(s)
                print('Deleting...')
                for f in self.args.f:
                    # you may have perm x but not d (to load or even do a head object)
                    # so use obj_exists

                    if self.aws.obj_exists(selected_area + f):

                        obj = s3_resource.ObjectSummary(self.aws.bucket_name, selected_area + f)
                        obj.delete()
                        print(selected_area + f + '  Done.')
                    else:
                        print(selected_area + f + '  File not found.')
                return

        except Exception as e:
            print_err(e, 'delete')


def delete_dir_perms_from_bucket_policy(s3_res, bucket_name, dir_name):
    try:
        bucket_policy = s3_res.BucketPolicy(bucket_name)
        policy_str = bucket_policy.policy
    except ClientError:
        policy_str = ''

    if policy_str:
        policy_json = json.loads(policy_str)
        changed = False
        for stmt in policy_json['Statement']:
            if dir_name in stmt['Resource']:
                policy_json['Statement'].remove(stmt)
                changed = True
        if changed:
            updated_policy = json.dumps(policy_json)
            bucket_policy.put(Policy=updated_policy)
