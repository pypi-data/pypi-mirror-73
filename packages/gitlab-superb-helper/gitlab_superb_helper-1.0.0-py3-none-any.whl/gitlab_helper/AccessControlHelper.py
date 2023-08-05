import gitlab


class AccessControlHelper:

    def __init__(self, gitlabUrl, gitlabKey):
        self.gitlabConnection = gitlab.Gitlab(gitlabUrl, gitlabKey)
        self.gitlabConnection.auth()

    def _listarRepositorios(self):
        print("Obtendo lista de repositórios no GitLab...")
        projects = self.gitlabConnection.projects.list(all=True)
        print("Total de repositórios: ", len(projects))
        return projects

    def _consultarRepositorios(self, projectGroupId):
        print(f"Obtendo lista de repositórios pertencentes ao grupo {projectGroupId} no GitLab...")
        group = self.gitlabConnection.groups.get(projectGroupId)
        groupProjects = group.projects.list(all=True, include_subgroups=True)
        print("Total de repositórios: ", len(groupProjects))
        projects = []
        for groupProject in groupProjects:
            projects.append(self.gitlabConnection.projects.get(groupProject.id))
        return projects

    def _obterRepositorio(self, projectId):
        return self.gitlabConnection.projects.get(projectId)

    def _consultarGruposPorNome(self, name):
        groups = self.gitlabConnection.groups.list(all=True, include_subgroups=True, search=name)
        return list(filter(lambda x: name == x.name.strip(), groups))

    def _obterGrupo(self, groupId):
        return self.gitlabConnection.groups.get(groupId)

    def _consultarUsuariosGrupo(self, group):
        return group.members.list()

    def _concederAcessoProjeto(self, project, userGroupId, nivelAcesso, verbose):
        baseLog = f"[groupId: {userGroupId}, projectId: {project.id}, projectName: {project.name_with_namespace.replace(' ', '')}, nível de acesso: {nivelAcesso}]"
        try:
            project.share(userGroupId, nivelAcesso)
            print(f"Acesso concedido: {baseLog}")
        except gitlab.exceptions.GitlabCreateError:
            if verbose:
                print(f"Acesso já existente: {baseLog}")
        except:
            if verbose:
                print(f"Erro ao conceder acesso: {baseLog}")

    def _concederAcessoGrupo(self, subGrupo, userId, nivelAcesso, verbose):
        baseLog = f"[userId: {userId}, groupId: {subGrupo.id}, groupName: {subGrupo.attributes['web_url'].replace('http://10.129.178.173/groups/', '')}, nível de acesso: {nivelAcesso}]"
        try:
            subGrupo.members.create({'user_id': userId, 'access_level': nivelAcesso})
            print(f"Acesso concedido: {baseLog}")
        except gitlab.exceptions.GitlabCreateError:
            if verbose:
                print(f"Acesso já existente: {baseLog}")
        except:
            if verbose:
                print(f"Erro ao conceder acesso: {baseLog}")

    def _striplist(self, l):
        return [x.strip() for x in l]

    def concederAcessoTodosRepositorios(self, userGroupId, nivelAcesso, verbose):
        projects = self._listarRepositorios()
        for project in projects:
            self._concederAcessoProjeto(project, userGroupId, nivelAcesso, verbose)

    def concederAcessoGrupoUsuariosGrupoRepositorios(self, projectGroupId, userGroupId, nivelAcesso, verbose):
        projects = self._consultarRepositorios(projectGroupId)
        for project in projects:
            self._concederAcessoProjeto(project, userGroupId, nivelAcesso, verbose)

    def concederAcessoGrupoUsuariosRepositorio(self, projectId, userGroupId, nivelAcesso, verbose):
        project = self._obterRepositorio(projectId)
        self._concederAcessoProjeto(project, userGroupId, nivelAcesso, verbose)

    def concederAcessoGrupoUsuariosSubGrupo(self, subGrupo, userGroupId, nivelAcesso, verbose):
        usuarios = self._consultarUsuariosGrupo(self._obterGrupo(userGroupId))
        subgroups = self._consultarGruposPorNome(subGrupo)
        for subgroup in subgroups:
            for usuario in usuarios:
                self._concederAcessoGrupo(subgroup, usuario.id, nivelAcesso, verbose)
