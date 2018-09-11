import os
import sys
import requests
import time

from settings import settings


def upload_file(dataset, directory_name, file_name, s):
    try:
        start = time.clock()
        print 'uploading {} to dataset {}'.format(os.path.join(directory_name, file_name), dataset)
        res = s.post(
            data_portal + '/api/action/resource_create',
            data={
                'id': '',
                'url': '',
                'gstar_path': '',
                'image_upload': '',
                'this_name': file_name,
                'clear_upload': '',
                'package_id': dataset,
                'description': '',
                'format': '',
                'dataproduct_type': '',
                'calib_level': '',
                'target_name': '',
                'terms_and_conditions': '',
                'name': file_name,
            },
            files=[('upload', file(os.path.join(directory_name, file_name)))],
        )
        if res.status_code == 200:
            print 'File {} from directory {} uploaded successfully!!'.format(file_name, directory_name)
        else:
            print 'Error uploading file. Error code {}'.format(res.status_code)
        end = time.clock()
        print 'Time taken {}'.format(end - start)
    except:
        pass


def upload_directory(dataset, directory, s):
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if os.path.isdir(path):
            continue
        else:
            upload_file(dataset, directory, file_name, s)


if __name__ == '__main__':
    '''
    This function gets a directory name and upload its files to an existing dataset in data-portal
    Any subdirectory is currently ignored, however that can be easily achieved by recursively 
    calling the upload_directory function
    '''
    if not len(sys.argv[1:]) == 2:
        print 'usage: python bulkupload.py dataset_id /directory/path'
        print 'dataset-id: id of ckan dataset where the files will be uploaded'
        print '/directory/path: the directory containing the files to be uploaded'
        exit(0)

    dataset_id = sys.argv[1]
    directory_path = sys.argv[2]

    if not os.path.exists(directory_path):
        print 'directory does not exist'
        exit(0)

    data_portal = settings.CKAN_HOST

    # check if dataset is there
    response = requests.get(
        data_portal + '/api/action/package_show?id=' + dataset_id
    )

    if not response.status_code == 200:
        print 'Dataset does not exist'
        exit(0)

    # creating a session
    session = requests.Session()

    # login user
    session.post(
        data_portal + '/login_generic?came_from=/user/logged_in',
        data={
            'login': settings.CKAN_USERNAME,
            'password': settings.CKAN_PASSWORD,
        }
    )

    upload_directory(dataset_id, directory_path, session)
