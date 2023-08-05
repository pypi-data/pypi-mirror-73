# GitLab Helper

This is an open source tool to help manage GitLab.

## Pre-requisites

Install the dependencies
+ pip3 install -r requirements.txt

## Scripts

**1. CloneUpdateGroup.py** - Clones all the projects of a group in their respective path structure
    
    python3 CloneUpdateGroup.py --url="" --token="" --userGroupId="" basePath=""

**2. ConcederAcessoListaGrupoUsuariosListaProjetos.py** - Grants access to a list of user groups in a list of projects:
    
    python3 ConcederAcessoListaGrupoUsuariosListaProjetos.py --url="" --token="" --userGroupIdList="" --projectIdList="" --nivelAcesso="" --verbose=""
    
**3. ConcederAcessoFull.py** - Grants access to all GitLab projects (repositories):
    
    python3 ConcederAcessoFull.py --url="" --token="" --userGroupId="" nivelAcesso="" --verbose=""
    
**4. ConcederAcessoGrupoUsuariosGrupoProjetos.py** - Grants access to a group of users in all repositories from a group project:
    
    python3 ConcederAcessoGrupoUsuariosGrupoProjetos.py --url="" --token="" --projectGroupId="" --userGroupId="" --nivelAcesso="" --verbose=""
    
**5. ConcederAcessoGrupoUsuariosSubgrupoProjetos.py** - Grants access to a group of users in all projects (and subprojects) with a specific name group:
    
    python3 ConcederAcessoGrupoUsuariosSubgrupoProjetos.py --url="" --token="" --subGrupo="" --userGroupId="" --nivelAcesso="" --verbose=""
    
