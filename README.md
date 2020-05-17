ocp_users
=========

OpenShift Conatiner Platform でユーザー管理を行うAnsible Role。

## Description

サポートしている[アイデンティティープロバイダー](https://access.redhat.com/documentation/ja-jp/openshift_container_platform/4.4/html/authentication/supported-identity-providers)はHTPasswdのみ。

### できること

- ユーザーの作成
  - [HTPasswd Secret の新規作成 or 編集](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.4/html-single/authentication/index#identity-provider-creating-htpasswd-secret_configuring-htpasswd-identity-provider)
  - [HTPasswd CR の編集](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.4/html-single/authentication/index#identity-provider-htpasswd-CR_configuring-htpasswd-identity-provider)
  - `ClusterRoleBinding` の作成（"既存の"Roleと作成したユーザーの紐付け）

- ユーザーの削除
  - [HTPasswd Secret の編集 or 削除](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.4/html-single/authentication/index#identity-provider-htpasswd-update-users_configuring-htpasswd-identity-provider) Secretの中身が空の場合はSecretを削除する
  - [HTPasswd CR の編集](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.4/html-single/authentication/index#identity-provider-htpasswd-CR_configuring-htpasswd-identity-provider) 登録されているHTPasswd Secretの中身が空の場合は登録を削除する
  - `User`オブジェクトの削除
  - `Identity`オブジェクトの削除
  - `ClusterRoleBinding` の削除

### できないこと

- `Group` の作成
- `User`を`Group`へ追加
- `Role` の作成
- 本Role以外で作成したユーザーの削除


## Requirement

- python >= 2.7
- Ansible >= 2.9
- openshift >= 0.6
- PyYAML >= 3.11

## Usage

各パラメタの説明は`defaults/main.yml` に記載。

### Example

ユーザー作成

``` yaml
- hosts: localhost
  connection: local
  vars:
    ocp_users_host: https://api.xxx.xxx.xxx:6443
    ocp_users_api_key: XXXXX
    ocp_users_validate_certs: False
    ocp_users_status: present
    ocp_users_users:
    - name: admin
      password: XXXXX
      crbs:
      - name: "cluster-admin-admin"
        clusterrole: cluster-admin
    - name: user1
      password: XXXXX
      crbs: []
    - name: user2
      password: XXXXX
      crbs:
      - name: "cluster-reader-user2"
        clusterrole: cluster-reader
      - name: "cluster-monitoring-view-user2"
        clusterrole: cluster-monitoring-view
  module_defaults:
    group/k8s:
      host: "{{ ocp_users_host }}"
      api_key: "{{ ocp_users_api_key }}"
      validate_certs: "{{ ocp_users_validate_certs }}"
  tasks:
  - name: ユーザー作成
    import_role:
      name: ocp_users
```

ユーザー削除

``` yaml
- hosts: localhost
  connection: local
  vars:
    ocp_users_host: https://api.xxx.xxx.xxx:6443
    ocp_users_api_key: XXXXX
    ocp_users_validate_certs: False
    ocp_users_status: absent
    ocp_users_users:
    - name: admin
      crbs:
      - name: cluster-admin-admin
    - name: user1
      crbs: []
    - name: user2
      crbs:
      - name: cluster-reader-user2
      - name: cluster-monitoring-view-user2
  module_defaults:
    group/k8s:
      host: "{{ ocp_users_host }}"
      api_key: "{{ ocp_users_api_key }}"
      validate_certs: "{{ ocp_users_validate_certs }}"
  tasks:
  - name: ユーザー削除
    import_role:
      name: ocp_users
```

## 参考

- [RedHat Customer Portal - Authentication](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.4/html-single/authentication/index)

## LICENSE
- MIT