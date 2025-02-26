"""
Tests for Image Management Service (IMS) CLI subcommand (`cray ims`)
and options.

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
# pylint: disable=unused-argument
import json
import os

from ..utils.runner import cli_runner  # pylint: disable=unused-import
from ..utils.rest import rest_mock  # pylint: disable=unused-import
from ..utils.utils import new_random_string


def compare_output(expected, cli_output):
    """
    Function helper to test if the expected values can
    be found in the output text.
    """
    found = False
    actual = [elem.strip() for elem in cli_output.splitlines()]
    for i, e in reversed(list(enumerate(actual))):
        if ':' in e:
            found = True
            del actual[0:i+1]
            break
    assert found
    assert set(expected) == set(actual)


# pylint: disable=redefined-outer-name
def test_cray_ims_base(cli_runner, rest_mock):
    """ Test cray ims base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims'])
    assert result.exit_code == 0

    outputs = [
        "deleted",
        "public-keys",
        "recipes",
        "images",
        "jobs"
    ]

    compare_output(outputs, result.output)


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_base(cli_runner, rest_mock):
    """ Test cray ims base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted'])
    assert result.exit_code == 0

    outputs = [
        "public-keys",
        "recipes",
        "images",
    ]

    compare_output(outputs, result.output)


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_base(cli_runner, rest_mock):
    """ Test cray ims public-keys base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "deleteall",
        "describe",
        "list",
    ]

    compare_output(outputs, result.output)


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_delete(cli_runner, rest_mock):
    """ Test cray ims public_keys delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/public-keys/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_delete_all(cli_runner, rest_mock):
    """ Test cray ims public_keys delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/public-keys'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_list(cli_runner, rest_mock):
    """ Test cray ims public_keys list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/public-keys'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_describe(cli_runner, rest_mock):
    """ Test cray ims public_keys describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'public-keys', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/public-keys/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_create(cli_runner, rest_mock):
    """ Test cray ims public_keys create ... happy path """
    runner, cli, config = cli_runner
    usersshpubkeyfile = os.path.join(
        os.path.dirname(__file__),
        '../files/text.txt'
    )
    result = runner.invoke(
        cli,
        ['ims', 'public-keys', 'create', '--name', 'foo',
         '--public-key', usersshpubkeyfile]
    )
    with open(usersshpubkeyfile, encoding='utf-8') as inf:
        pubkeydata = inf.read()
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/v3/public-keys'.format(
        config['default']['hostname']
    )
    assert data['body'] == {
        'name': 'foo',
        'public_key': pubkeydata
    }


# pylint: disable=redefined-outer-name
def test_cray_ims_public_keys_create_missing_required(cli_runner, rest_mock):
    """Test cray ims public_keys create ... when a required parameter is
    missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(
        cli,
        ['ims', 'public-keys', 'create', '--name', 'foo']
    )
    assert result.exit_code == 2
    assert '--public-key' in result.output


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_public_keys_base(cli_runner, rest_mock):
    """ Test cray ims public-keys base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'public-keys'])
    assert result.exit_code == 0

    outputs = [
        "update",
        "delete",
        "deleteall",
        "describe",
        "list",
    ]

    compare_output(outputs, result.output)

# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_public_keys_delete(cli_runner, rest_mock):
    """ Test cray ims public_keys delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'public-keys', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/deleted/public-keys/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_public_keys_delete_all(cli_runner, rest_mock):
    """ Test cray ims public_keys delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'public-keys', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/deleted/public-keys'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_public_keys_update(cli_runner, rest_mock):
    """ Test cray ims deleted public_keys update ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'public-keys', 'update', 'foo',
                                 '--operation', 'undelete'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}/apis/ims/v3/deleted/public-keys/foo'.format(
        config['default']['hostname']
    )
    assert data['body'] == {
    'operation': 'undelete'
    }


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_public_keys_list(cli_runner, rest_mock):
    """ Test cray ims deleted public_keys list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'public-keys', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/deleted/public-keys'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_public_keys_describe(cli_runner, rest_mock):
    """ Test cray ims deleted public_keys describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'public-keys', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/deleted/public-keys/foo'.format(
        config['default']['hostname']
    )

# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_base(cli_runner, rest_mock):
    """ Test cray ims recipes base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "deleteall",
        "describe",
        "list",
        "update"
    ]

    compare_output(outputs, result.output)

# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_delete(cli_runner, rest_mock):
    """ Test cray ims recipes delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/recipes/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_delete_all(cli_runner, rest_mock):
    """ Test cray ims recipes delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/recipes'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_list(cli_runner, rest_mock):
    """ Test cray ims recipes list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/recipes'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_describe(cli_runner, rest_mock):
    """ Test cray ims recipes describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'recipes', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/recipes/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_create(cli_runner, rest_mock):
    """ Test cray ims recipes create ... happy path """
    runner, cli, config = cli_runner
    s3_link_path = new_random_string()
    s3_link_etag = new_random_string()
    result = runner.invoke(cli, ['ims', 'recipes', 'create',
                                 '--name', 'foo',
                                 '--linux-distribution', 'sles15',
                                 '--recipe-type', 'kiwi-ng',
                                 '--link-type', 's3',
                                 '--link-path', s3_link_path,
                                 '--link-etag', s3_link_etag])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/v3/recipes'.format(
        config['default']['hostname']
    )
    assert data['body'].get('name', None) == 'foo'
    assert data['body'].get('linux_distribution', None) == 'sles15'
    assert data['body'].get('recipe_type', None) == 'kiwi-ng'
    assert 'link' in data['body']
    assert data['body']['link'].get('type', None) == 's3'
    assert data['body']['link'].get('path', None) == s3_link_path
    assert data['body']['link'].get('etag', None) == s3_link_etag


# pylint: disable=redefined-outer-name
def test_cray_ims_recipes_create_missing_required(cli_runner, rest_mock):
    """Test cray ims recipes create ... when a required parameter is
    missing

    """
    runner, cli, _ = cli_runner
    result = runner.invoke(
        cli,
        ['ims', 'recipes', 'create',
         '--name', 'foo',
         '--recipe-type', 'kiwi-ng']
    )
    assert result.exit_code == 2
    assert '--linux-distribution' in result.output


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_recipes_base(cli_runner, rest_mock):
    """ Test cray ims recipes base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'recipes'])
    assert result.exit_code == 0

    outputs = [
        "update",
        "delete",
        "deleteall",
        "describe",
        "list",
    ]

    compare_output(outputs, result.output)

# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_recipes_delete(cli_runner, rest_mock):
    """ Test cray ims recipes delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'recipes', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/deleted/recipes/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_recipes_delete_all(cli_runner, rest_mock):
    """ Test cray ims recipes delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'recipes', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/deleted/recipes'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_recipes_update(cli_runner, rest_mock):
    """ Test cray ims deleted recipes update ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'recipes', 'update', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}/apis/ims/v3/deleted/recipes/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_recipes_list(cli_runner, rest_mock):
    """ Test cray ims deleted recipes list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'recipes', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/deleted/recipes'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_recipes_describe(cli_runner, rest_mock):
    """ Test cray ims deleted recipes describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'recipes', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/deleted/recipes/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_images_base(cli_runner, rest_mock):
    """ Test cray ims images base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'images'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "deleteall",
        "describe",
        "list",
        "update"
    ]

    compare_output(outputs, result.output)

# pylint: disable=redefined-outer-name
def test_cray_ims_images_delete(cli_runner, rest_mock):
    """ Test cray ims images delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/images/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_images_delete_all(cli_runner, rest_mock):
    """ Test cray ims images delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/images'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_images_list(cli_runner, rest_mock):
    """ Test cray ims images list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/images'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_images_describe(cli_runner, rest_mock):
    """ Test cray ims images describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/images/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_images_create(cli_runner, rest_mock):
    """ Test cray ims images create ... happy path """
    runner, cli, config = cli_runner
    s3_link_path = new_random_string()
    s3_link_etag = new_random_string()
    result = runner.invoke(cli, ['ims', 'images', 'create',
                                 '--name', 'foo',
                                 '--link-type', 's3',
                                 '--link-path', s3_link_path,
                                 '--link-etag', s3_link_etag])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/v3/images'.format(
        config['default']['hostname']
    )
    assert 'name' in data['body'] and data['body']['name'] == 'foo'
    assert 'link' in data['body']
    assert data['body']['link'].get('type', None) == 's3'
    assert data['body']['link'].get('path', None) == s3_link_path
    assert data['body']['link'].get('etag', None) == s3_link_etag


# pylint: disable=redefined-outer-name
def test_cray_ims_images_create_missing_required(cli_runner, rest_mock):
    """ Test cray ims images create ... happy path """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'images', 'create'])
    assert result.exit_code == 2
    assert '--name' in result.output


# pylint: disable=redefined-outer-name
def test_cray_ims_images_update(cli_runner, rest_mock):
    """ Test cray ims images update ... """
    runner, cli, config = cli_runner
    test_link_type = 's3'
    test_link_etag = new_random_string()
    test_link_path = new_random_string()
    result = runner.invoke(cli, ['ims', 'images', 'update', 'foo',
                                 '--link-type', test_link_type,
                                 '--link-etag', test_link_etag,
                                 '--link-path', test_link_path])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}/apis/ims/v3/images/foo'.format(
        config['default']['hostname']
    )
    assert data['body'] == {
        'link': {
            'type': test_link_type,
            'etag': test_link_etag,
            'path': test_link_path
        }
    }


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_images_base(cli_runner, rest_mock):
    """ Test cray ims images base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'images'])
    assert result.exit_code == 0

    outputs = [
        "update",
        "delete",
        "deleteall",
        "describe",
        "list",
    ]

    compare_output(outputs, result.output)

# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_images_delete(cli_runner, rest_mock):
    """ Test cray ims images delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'images', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/deleted/images/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_images_delete_all(cli_runner, rest_mock):
    """ Test cray ims images delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'images', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/deleted/images'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_images_update(cli_runner, rest_mock):
    """ Test cray ims deleted images update ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'images', 'update', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'PATCH'
    assert data['url'] == '{}/apis/ims/v3/deleted/images/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_images_list(cli_runner, rest_mock):
    """ Test cray ims deleted images list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'images', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/deleted/images'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_deleted_images_describe(cli_runner, rest_mock):
    """ Test cray ims deleted images describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'deleted', 'images', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/deleted/images/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_base(cli_runner, rest_mock):
    """ Test cray ims jobs base command """
    runner, cli, _ = cli_runner
    result = runner.invoke(cli, ['ims', 'jobs'])
    assert result.exit_code == 0

    outputs = [
        "create",
        "delete",
        "deleteall",
        "describe",
        "list",
    ]
    compare_output(outputs, result.output)


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_delete(cli_runner, rest_mock):
    """ Test cray ims jobs delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'jobs', 'delete', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/jobs/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_delete_all(cli_runner, rest_mock):
    """ Test cray ims jobs delete ... """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'jobs', 'deleteall'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'DELETE'
    assert data['url'] == '{}/apis/ims/v3/jobs'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_list(cli_runner, rest_mock):
    """ Test cray ims jobs list """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'jobs', 'list'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/jobs'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_describe(cli_runner, rest_mock):
    """ Test cray ims jobs describe """
    runner, cli, config = cli_runner
    result = runner.invoke(cli, ['ims', 'jobs', 'describe', 'foo'])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'GET'
    assert data['url'] == '{}/apis/ims/v3/jobs/foo'.format(
        config['default']['hostname']
    )


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_create_create(cli_runner, rest_mock):
    """ Test cray ims jobs create ... happy path """
    runner, cli, config = cli_runner
    test_build_env_size = '15'
    test_enable_debug = 'True'
    test_public_key = new_random_string()
    test_artifact_id = new_random_string()
    test_initrd_file_name = new_random_string()
    test_kernel_file_name = new_random_string()
    test_image_root_archive_name = new_random_string()
    test_job_type = "create"
    result = runner.invoke(
        cli,
        ['ims', 'jobs', 'create',
         '--build-env-size', test_build_env_size,
         '--enable-debug', test_enable_debug,
         '--public-key-id', test_public_key,
         '--artifact-id', test_artifact_id,
         '--initrd-file-name', test_initrd_file_name,
         '--kernel-file-name', test_kernel_file_name,
         '--image-root-archive-name', test_image_root_archive_name,
         '--job-type', test_job_type]

    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/v3/jobs'.format(
        config['default']['hostname']
    )
    assert data['body'] == {
        'build_env_size': int(test_build_env_size),
        'enable_debug': True,
        'public_key_id': test_public_key,
        'artifact_id': test_artifact_id,
        'initrd_file_name': test_initrd_file_name,
        'kernel_file_name': test_kernel_file_name,
        'image_root_archive_name': test_image_root_archive_name,
        'job_type': test_job_type
    }


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_create_customize(cli_runner, rest_mock):
    """ Test cray ims jobs create ... happy path """
    runner, cli, config = cli_runner
    test_build_env_size = '15'
    test_enable_debug = 'True'
    test_public_key = new_random_string()
    test_artifact_id = new_random_string()
    test_initrd_file_name = new_random_string()
    test_kernel_file_name = new_random_string()
    test_image_root_archive_name = new_random_string()
    test_job_type = "customize"
    result = runner.invoke(
        cli,
        ['ims', 'jobs', 'create',
         '--build-env-size', test_build_env_size,
         '--enable-debug', test_enable_debug,
         '--public-key-id', test_public_key,
         '--artifact-id', test_artifact_id,
         '--initrd-file-name', test_initrd_file_name,
         '--kernel-file-name', test_kernel_file_name,
         '--image-root-archive-name', test_image_root_archive_name,
         '--job-type', test_job_type]

    )
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data['method'] == 'POST'
    assert data['url'] == '{}/apis/ims/v3/jobs'.format(
        config['default']['hostname']
    )
    assert data['body'] == {
        'build_env_size': int(test_build_env_size),
        'enable_debug': True,
        'public_key_id': test_public_key,
        'artifact_id': test_artifact_id,
        'initrd_file_name': test_initrd_file_name,
        'kernel_file_name': test_kernel_file_name,
        'image_root_archive_name': test_image_root_archive_name,
        'job_type': test_job_type,
    }


# pylint: disable=redefined-outer-name
def test_cray_ims_jobs_create_missing_required(cli_runner, rest_mock):
    """Test cray ims jobs create ... when a required parameter is
    missing

    """
    runner, cli, _ = cli_runner
    test_public_key = new_random_string()
    test_artifact_id = new_random_string()
    test_job_type = "customize"
    result = runner.invoke(
        cli,
        ['ims', 'jobs', 'create',
         '--public-key-id', test_public_key,
         '--artifact-id', test_artifact_id,
         '--job-type', test_job_type]
    )
    assert result.exit_code == 2
    assert '--image-root-archive-name' in result.output
