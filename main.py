import requests
import re

def get_session():
    session = requests.Session()
    session.auth = (user, password)
    return session


def project():
    x = get_session().get('{url}/api/v2.0/projects?page=1&page_size=10&with_detail=true')
    x.raise_for_status()
    return x.json()


def repository(project):
    x = get_session().get(f'{url}/api/v2.0/projects/{project}/repositories', headers={'X-Is-Resource-Name': 'true'})
    x.raise_for_status()
    return x.json()


def tag(project, service):
    x = get_session().get(f'{url}/api/v2.0/projects/{project}/repositories/{service}/artifacts?page=1&page_size=10&with_tag=true&with_label=false&with_scan_overview=false&with_sbom_overview=false&with_signature=false&with_immutable_status=false&with_accessory=false')
    x.raise_for_status()
    return x.json()

if __name__ == '__main__':
    user = "user"
    password = "password"
    url = "https://example.com"
    projects = project()
    for project in projects:
        repositorys = repository(project['name'])
        for item in repositorys:
            service = item['name'].split('/')[1]
            artifacts = tag(project['name'], service)
            for artifact in artifacts:
                for version in artifact['tags']:
                    print(f"harbor.hellking.dev/{project['name']}/{service}:{version['name']}")
