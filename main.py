from os import system

import requests
import re
import subprocess


def get_session():
    session = requests.Session()
    session.auth = (user, password)
    return session


def project():
    x = get_session().get('https://harbor.hellking.dev/api/v2.0/projects?page=1&page_size=10&with_detail=true')
    x.raise_for_status()
    return x.json()


def repository(project):
    x = get_session().get(f'https://harbor.hellking.dev/api/v2.0/projects/{project}/repositories',
                          headers={'X-Is-Resource-Name': 'true'})
    x.raise_for_status()
    return x.json()


def tag(project, service):
    x = get_session().get(
        f'https://harbor.hellking.dev/api/v2.0/projects/{project}/repositories/{service}/artifacts?page=1&page_size=10&with_tag=true&with_label=false&with_scan_overview=false&with_sbom_overview=false&with_signature=false&with_immutable_status=false&with_accessory=false')
    x.raise_for_status()
    return x.json()

def convert_image_name(image):
    parts = image.split('/')
    image_name, tag = parts[-1].split(':')
    return f"phananhthoai/projects:{image_name}-{tag}"

if __name__ == '__main__':
    print('Starting ...')
    user = "admin"
    password = "Harbor12345"
    projects = project()
    images = []
    for project in projects:
        print(f'Found project {project}')
        repositorys = repository(project['name'])
        for item in repositorys:
            print(f'Found repository {item}')
            service = item['name'].split('/')[1]
            artifacts = tag(project['name'], service)
            for artifact in artifacts:
                for version in artifact['tags']:
                    images.append(f"harbor.hellking.dev/{project['name']}/{service}:{version['name']}")
                    # print(f"harbor.hellking.dev/{project['name']}/{service}:{version['name']}")

    for image in images:
        print(f'Pulling {image} ...')
        system(f'docker pull {image}')
        docker_image = convert_image_name(image)
        system(f'docker tag {image} {docker_image}')
        system(f'docker push {docker_image}')
    print('OK')
