import os
from pathlib import Path
import gitlab


class CloneSyncHelper:

    def __init__(self, gitlabUrl, gitlabKey):
        self.gitlabConnection = gitlab.Gitlab(gitlabUrl, gitlabKey)
        self.gitlabConnection.auth()

    def _consultarRepositorios(self, projectGroupId):
        print(f"Obtendo lista de repositórios pertencentes ao grupo {projectGroupId} no GitLab...")
        group = self.gitlabConnection.groups.get(projectGroupId)
        groupProjects = group.projects.list(all=True, include_subgroups=True)
        print("Total de repositórios: ", len(groupProjects))
        return groupProjects

    def _formatarRepositorios(self, groups):
        _sshUrls = dict()
        for group in groups:
            _sshUrls.update({group.attributes['name_with_namespace']: group.attributes['ssh_url_to_repo']})
        return _sshUrls

    def _getFullRepositoryPath(self, basePath, repoFolderStructure):
        repoPath = repoFolderStructure.replace(" / ", "\\").strip()
        fullPath = f'{basePath}\\{repoPath}'
        return Path(fullPath)

    def _createDirectoryStructure(self, basePath, repoFolderStructure):
        path = self._getFullRepositoryPath(basePath, repoFolderStructure)
        path.parent.mkdir(parents=True, exist_ok=True)
        print(f'Directory created: {path}')
        return str(path)

    def _cloneRepository(self, path, url):
        splittedPath = os.path.split(path)
        os.chdir(splittedPath[0])
        print(f'Cloning: {splittedPath[1]}')
        stream = os.popen(f'git clone {url}')
        output = stream.read()
        print(output)

    def _updateRepository(self, path):
        splittedPath = os.path.split(path)
        os.chdir(path)
        print(f'Updating: {splittedPath[-1]}')
        stream = os.popen(f'git pull --rebase')
        output = stream.read()
        print(output)

    def cloneUpdateGroup(self, projectGroupId, basePath):
        _groups = self._consultarRepositorios(projectGroupId)
        _sshUrls = self._formatarRepositorios(_groups)
        for repo, url in _sshUrls.items():
            fullPath = self._getFullRepositoryPath(basePath, repo)
            if os.path.exists(f"{fullPath}\\.git"):
                self._updateRepository(fullPath)
                continue
            path = self._createDirectoryStructure(basePath, repo)
            self._cloneRepository(path, url)