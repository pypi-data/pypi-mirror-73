'''
解析mysql请求步骤的.
解析类似下面的json
{
    "name": "测试步骤1",
    "type": "mysql",
    "wait":{
       "retry":"",
       "retryInterval"
    },
    "input": {
        "sql": "select * from table where id=1",
        "config": {
            "host":"127.0.0.1",
            "port":3306,  #默认是3306，string类型也可以
            "user":"root",
            "password":"password",
            "db":"database"
        }
    },
    "expect": {
        "expect_count": "${1}",
        "expect_result": [{
            "aa": "213"
        }],
        "expect_contains":{<字典或者列表>},
        "should_be_none":True
    }
}
'''
from builtins import dict, isinstance, str, int

from xforceCloudTestBasic import statusObj as statusObj
from xfctRftBasic import typeUtils as typeUtils
import re

_STEP_NAME='name'
_INPUT='input'
_EXPECT='expect'
_SQL='sql'
_CONFIG='config'
_HOST='host'
_PORT='port'
_USER='user'
_PASSWORD='password'
_DB='db'
_EXPECT_COUNT='expect_count'
_EXPECT_RESULT='expect_result'
_EXPECT_CONTAINS='expect_contains'
_SHOULD_BE_NONE='should_be_none'

_BLOCK=" " * 4
_SEPERATE=" " * 2
_KEY_WORD='At Run Sql'
_STEP_TYPE='mysql'

_STEP_WAIT="wait"
_STEP_WAIT_RETRY="retry"
_STEP_WAIT_RETRY_INTERVAL="retryInterval"
_WAIT_KEYWORD="Wait until keyword succeeds"


def parse(file_path, suite_name,case_name,step_detail_json):
    '''
    检查http步骤是否有效。
    :param step_detail_json:
    :return:
    '''
    if not isinstance(step_detail_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, _STEP_TYPE,'测试步骤不是字典')
    if _STEP_NAME not in step_detail_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, _STEP_TYPE, '测试步骤不存在'+_STEP_NAME)
    if not isinstance(step_detail_json[_STEP_NAME],str):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, None, _STEP_TYPE, '测试步骤' + _STEP_NAME+'不是string类型')
    step_name=step_detail_json[_STEP_NAME]

    content = _BLOCK + '${' + step_name + '}='
    if _STEP_WAIT in step_detail_json and step_detail_json[_STEP_WAIT] is not None:
        wait = step_detail_json[_STEP_WAIT]
        if not isinstance(wait, dict):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "不是dict类型")
        if _STEP_WAIT_RETRY not in wait:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里" + _STEP_WAIT_RETRY + "不存在")
        if _STEP_WAIT_RETRY_INTERVAL not in wait:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里" + _STEP_WAIT_RETRY_INTERVAL + "不存在")
        wait_retry = wait[_STEP_WAIT_RETRY]
        wait_retry_interval = wait[_STEP_WAIT_RETRY_INTERVAL]
        if not isinstance(wait_retry, str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE, '测试步骤' + _STEP_WAIT + "里" + _STEP_WAIT_RETRY + "不是str类型")
        if not isinstance(wait_retry_interval, str):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                              _STEP_TYPE,
                                              '测试步骤' + _STEP_WAIT + "里" + _STEP_WAIT_RETRY_INTERVAL + "不是str类型")
        content += _SEPERATE + _WAIT_KEYWORD + _SEPERATE + wait_retry + _SEPERATE + wait_retry_interval

    content += _SEPERATE + _KEY_WORD

    if _INPUT not in step_detail_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE,_INPUT+'是必填字段')
    input_json=step_detail_json[_INPUT]
    if not isinstance(input_json,dict):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE,_INPUT + '字段' + str(input_json) +'不是字典')

    ##########################
    # sql和config是必填字段
    #########################
    if _SQL not in input_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _INPUT + '.' + _SQL + ']是必填字段')
    sql=input_json[_SQL]
    if not typeUtils.is_str(sql):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '['+_INPUT+'.'+_SQL + ']字段' +str(sql) +'不是string类型')
    #验证sql不能有多余2个以上空格或者换行符
    if not _check_valid_sql(sql):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _INPUT + '.' + _SQL + ']字段' + str(sql) + '里面有连续的空格符或者制表符')

    content+= _SEPERATE + sql
    if _CONFIG not in input_json:
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '['+_INPUT+'.'+_CONFIG + ']是必填字段')
    config=input_json[_CONFIG]

    if typeUtils.is_rft_variable(config):
        content += _SEPERATE + config

    elif not typeUtils.is_dict_or_dict_str(config):
        return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                    _STEP_TYPE, '['+_INPUT+'.'+_CONFIG + ']字段不是字典类型')
    else:
        new_config={}
        #验证host
        if _HOST not in config:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _INPUT + '.' + _CONFIG + '.'+ _HOST +']是必填字段')
        if not typeUtils.is_str(_HOST):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _INPUT + '.' + _CONFIG + '.' + _HOST + ']不是string类型')
        new_config.update({_HOST:config[_HOST]})
        #验证端口
        if _PORT not in config:
            #如果port不存在使用默认的3306
            new_config.update({_PORT: 3306})
        else:
            port=config[_PORT]
            if not typeUtils.is_int_or_int_str(port):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE, '[' + _EXPECT + '.' + _EXPECT_COUNT + ']字段' + str(port) + '是不支持的')
            port_int = typeUtils.get_int_value(port)
            if port_int <= 0:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _EXPECT + '.' + _EXPECT_COUNT + ']字段' + str(port_int) + '必须是正整数')
            new_config.update({_PORT: port_int})
        if _USER not in config:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _INPUT + '.' + _CONFIG + '.' + _USER + ']是必填字段')
        if not typeUtils.is_str(_USER):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE, '[' + _INPUT + '.' + _CONFIG + '.' + _USER + ']不是string类型')
        new_config.update({_USER:config[_USER]})
        if _PASSWORD not in config:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE,
                                          '[' + _INPUT + '.' + _CONFIG + '.' + _PASSWORD + ']是必填字段')
        if not typeUtils.is_str(_PASSWORD):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE,
                                          '[' + _INPUT + '.' + _CONFIG + '.' + _PASSWORD + ']不是string类型')
        new_config.update({_PASSWORD: config[_PASSWORD]})
        if _DB not in config:
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE,
                                          '[' + _INPUT + '.' + _CONFIG + '.' + _DB + ']是必填字段')
        if not typeUtils.is_str(_DB):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name, _STEP_TYPE,
                                          '[' + _INPUT + '.' + _CONFIG + '.' + _DB + ']不是string类型')
        new_config.update({_DB: config[_DB]})
        new_config.update({"charset": "utf8"})
        content += _SEPERATE + typeUtils.covert_json_or_json_str_to_json_formate_str(new_config)


    #########################################
    # 如果存在，检测status_code, resp_header,resp_body, resp_json, resp_body_contains, resp_json_contains
    #########################################
    if _EXPECT in step_detail_json and step_detail_json[_EXPECT] is not None:
        expect_json=step_detail_json[_EXPECT]
        if not isinstance(expect_json,dict):
            return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,_EXPECT + '字段' + str(expect_json) + '不是字典')
        #验证expect_count
        if _EXPECT_COUNT in expect_json and expect_json[_EXPECT_COUNT] is not None:
            expect_count=expect_json[_EXPECT_COUNT]
            if not typeUtils.is_str(expect_count) and not isinstance(expect_count,int):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _EXPECT + '.' + _EXPECT_COUNT + ']字段' + str(expect_count) + '不是string类型或者int类型')
            #检查expect_count是合理的数据
            if not typeUtils.is_int_or_int_str(expect_count):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                                _STEP_TYPE,'[' + _EXPECT + '.' + _EXPECT_COUNT + ']字段' + str(expect_count) + '是不支持的')
            expect_count_int=typeUtils.get_int_value(expect_count)
            if expect_count_int<0:
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE,'[' + _EXPECT + '.' + _EXPECT_COUNT + ']字段' + str(expect_count) + '必须是非负正整数')
            content+=_SEPERATE+ _EXPECT_COUNT+'=${'+ str(expect_count_int) +'}'
        #验证expect_result
        if _EXPECT_RESULT in expect_json and expect_json[_EXPECT_RESULT] is not None:
            if not typeUtils.is_list_or_list_str(expect_json[_EXPECT_RESULT]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                         _STEP_TYPE,'[' + _EXPECT + '.' + _EXPECT_RESULT + ']字段' + expect_json[_EXPECT_RESULT] + '不是list类型或者能转成list的string类型')
            content += _SEPERATE + _EXPECT_RESULT + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(expect_json[_EXPECT_RESULT])
        #验证expect_contains
        if _EXPECT_CONTAINS in expect_json and expect_json[_EXPECT_CONTAINS] is not None:
            if not typeUtils.is_dict_or_dict_str(expect_json[_EXPECT_CONTAINS]) and not typeUtils.is_list_or_list_str(expect_json[_EXPECT_CONTAINS]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                        _STEP_TYPE,'[' + _EXPECT + '.' + _EXPECT_CONTAINS + ']字段' + expect_json[_EXPECT_CONTAINS] + '不是list或者dict类型')
            content += _SEPERATE + _EXPECT_CONTAINS + '=' + typeUtils.covert_json_or_json_str_to_json_formate_str(expect_json[_EXPECT_CONTAINS])
        #验证should_be_none
        if _SHOULD_BE_NONE in expect_json and expect_json[_SHOULD_BE_NONE] is not None:
            if not typeUtils.is_bool_or_bool_str(expect_json[_SHOULD_BE_NONE]):
                return statusObj.get_step_content(file_path, statusObj.STATUS_NOK, suite_name, case_name, step_name,
                         _STEP_TYPE,'[' + _EXPECT + '.' + _SHOULD_BE_NONE + ']字段' + expect_json[_SHOULD_BE_NONE] + '不是bool类型')

            content += _SEPERATE + _SHOULD_BE_NONE + '=${' + str(typeUtils.get_bool_value(expect_json[_SHOULD_BE_NONE]))+'}'
    return statusObj.get_step_content(file_path, statusObj.STATUS_OK, suite_name, case_name, step_name,_STEP_TYPE, 'OK',content=content)

def get_settings_content():
    '''
    获取robot文件依赖。
    :return: content
    '''
    content = 'Library  rfApiTestLibrary/supper.py\n'
    return content

def _check_valid_sql(sql):
    '''
    检查sql是否符合robot framework的空格位子需求。
    :param sql: string类型。
    :return:
    '''
    new_sql=sql.replace("\n","")
    if re.search('^\${.*}$', new_sql) is not None:
        return True
    match = re.search(r'\s{2,}', new_sql)
    if match is not None:
        return False
    return True




