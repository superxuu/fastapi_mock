import time
from pathlib import Path
import yaml
import re
from fastapi import HTTPException
from fastapi.logger import logger

hash_dict = {}


class MockResponce():
    def __init__(self, api_group, api_name, request_args):
        self.api_group = api_group
        self.api_name = api_name
        self.request_args = request_args
        self.hash_key = hash(f'{self.api_group}@{self.api_name}@{self.request_args}')

    def responce_filter(self, read: bool = None):
        """
        :param read: 判断是否读取结果文件，True读取，返回结果文件的内容，适用于：Response(MockResponce('vba_api', 'vba1', json_body).responce_filter(read=True), media_type='application/json')
                                       Fase不读取，直接返回文件路径，只用于：FileResponse(MockResponce('vba_api', 'vba1', json_body).responce_filter(read=False))
        :return:
        """
        if not read:
            config = self._get_config()
            res_file_path = self._get_response_file(config)
            return res_file_path
        else:
            global hash_dict
            logger.info(f'hash_dict_len: {len(hash_dict)}')
            if self.hash_key in hash_dict:
                logger.info('hash_dict存在所要的响应，直接从hash_dict获取')
                return hash_dict[self.hash_key]
            else:
                config = self._get_config()
                res_file_path = self._get_response_file(config)
                response = open(res_file_path, 'r', encoding='UTF-8').read()
                hash_dict[self.hash_key] = response
                return response

    def _get_config(self):
        config_yaml = Path('apis/' + self.api_group + '/config/' + self.api_name + '.yaml')
        # print(config_yaml)
        if config_yaml.exists():
            config = yaml.load(open(config_yaml, encoding='UTF-8'))
            return config
        else:
            logger.error(f'Mock 规则文件{config_yaml}不存在！！！')
            raise HTTPException(status_code=404, detail=f"Mock yaml规则文件{config_yaml}不存在")

    def _get_response_file(self, config):
        res_list = config.get(self.api_name)
        for res in res_list:
            if res['enable'] in ['N', 'n']:
                continue
            else:
                condition_judge_list = []
                for con in res['condition']:
                    args_field = self._get_field_from_args(con['field'])
                    target_field = con['value']
                    relu = con['rule']
                    if self._exec_rule(relu, args_field, target_field):
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
            if self._get_json_keyvalue(self.request_args, field):
                return self._get_json_keyvalue(self.request_args, field)[0]
            else:
                return None  # 入参body关键字没传时

    @staticmethod
    def _get_json_keyvalue(input_json, field):
        """从json中取出关键key的所有value组成的list"""
        result = []

        def _get_keyvalue_all(input_json):
            if isinstance(input_json, dict):
                for key in input_json.keys():
                    key_value = input_json.get(key)
                    if isinstance(key_value, dict):
                        _get_keyvalue_all(key_value)
                    elif isinstance(key_value, list):
                        for json_array in key_value:
                            _get_keyvalue_all(json_array)
                    else:
                        if key == field:
                            result.append(key_value)
                return result
            elif isinstance(input_json, list):
                for input_json_array in input_json:
                    _get_keyvalue_all(input_json_array)

        return _get_keyvalue_all(input_json)

    @staticmethod
    def _exec_rule(rule, src, target):
        if rule == 'is':
            if src == None or src == '':
                return target in ['None', 'none']
            return src == target
        if rule == 'regex':
            return re.match(target, src)
