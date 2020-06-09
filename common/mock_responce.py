import time
from pathlib import Path
import yaml
import re
from fastapi import HTTPException
from fastapi.logger import logger

# from .log_config import getloger


# logger = getloger(__name__)


class MockResponce():
    def __init__(self, api_group, api_name, request_args):
        self.api_group = api_group
        self.api_name = api_name
        self.request_args = request_args
        self.config_yaml = Path('apis/' + self.api_group + '/config/' + self.api_name + '.yaml')
        # print(config_yaml)
        if self.config_yaml.exists():
            self.config = yaml.load(open(self.config_yaml, encoding='UTF-8'))
            # print(self.config)
            # print(self.api_name)
        else:
            logger.error(f'Mock 规则文件{self.config_yaml}不存在！！！')
            # print(f'Mock 规则文件{self.config_yaml}不存在！！！')
            raise HTTPException(status_code=404, detail=f"Mock yaml规则文件{self.config_yaml}不存在")

    def responce_filter(self):
        res_list = self.config.get(self.api_name)
        for res in res_list:
            if res['enable'] in ['N', 'n']:
                continue
            else:
                condition_judge_list=[]
                for con in res['condition']:
                    args_field = self._get_field_from_args(con['field'])
                    target_field = con['value']
                    relu = con['rule']
                    if self.exec_rule(relu, args_field, target_field):
                        condition_judge_list.append(True)
                    else:
                        condition_judge_list.append(False)
                if all(condition_judge_list):
                    logger.info(f'condition_judge_list:{condition_judge_list}')
                    delay = res.get('delay')
                    logger.info(
                        f'命中规则文件{self.api_name}第{res["index"]}条，延时{delay}秒，'
                        f'规则为：{relu}-{target_field}，输入为：{args_field}')
                    res_file_path = 'apis/' + self.api_group + '/responce_file/' + self.api_name + '/' + res[
                        'res_file']
                    time.sleep(0 if not delay else delay)
                    return res_file_path
        logger.error(f"{self.config_yaml}中无匹配规则：{args_field}")
        raise HTTPException(status_code=404, detail=f"{self.config_yaml}中无匹配规则：{args_field}")

    def _get_field_from_args(self, field):
        """
        从传过来的请求参数中取得field关键字的值
        传过来的参数request.query_params、request.form()不是字典，但是都可以直接request_args.get(field)取得值
        request.json()传过来的是字典
        request.body()传过来的绝大部分是字典，也可能是字符串，字符串暂时忽略
        """
        if isinstance(self.request_args, str):
            # TODO:  request.body()也可能是字符串，字符串暂时忽略,情况很少
            pass
        elif not isinstance(self.request_args, dict):
            return self.request_args.get(field)
        else:
            if self.get_json_keyvalue(self.request_args, field):
                return self.get_json_keyvalue(self.request_args, field)[0]
            else:
                return None  # 入参body关键字没传时

    @staticmethod
    def get_json_keyvalue(input_json, field):
        """从json中取出关键key的所有value组成的list"""
        result = []

        def get_keyvalue_all(input_json):
            if isinstance(input_json, dict):
                for key in input_json.keys():
                    key_value = input_json.get(key)
                    if isinstance(key_value, dict):
                        get_keyvalue_all(key_value)
                    elif isinstance(key_value, list):
                        for json_array in key_value:
                            get_keyvalue_all(json_array)
                    else:
                        if key == field:
                            result.append(key_value)
                return result
            elif isinstance(input_json, list):
                for input_json_array in input_json:
                    get_keyvalue_all(input_json_array)

        return get_keyvalue_all(input_json)

    def exec_rule(self, rule, src, target):
        if rule == 'is':
            if src == None or src == '':
                return target in ['None', 'none']
            return src == target
        if rule == 'regex':
            return re.match(target, src)
