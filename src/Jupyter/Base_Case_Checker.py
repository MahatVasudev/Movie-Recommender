import sys
import os
from dataclasses import dataclass, field 
import pickle
import time


@dataclass
class BaseCase:
    repo: str 
    data_repo: str = field(init=False)
    model_repo: str = field(init=False)
    
    def __post_init__(self):
        self.data_repo = self.repo + r'/data/'
        self.model_repo = self.repo + r'/model/'    
        self.model_files: list[str] = ['svd.pkl']
        self.data_files: list[str] = ['data_cleaned_v2.csv', 
        'genre_utility_matrix_with_movies.csv', 'ratings_cleaned.csv',
        'movies_cleaned.csv']


    def __connection_checker(self,status,file_in_question, extra) -> None:
        report_cache = {403: f"\033[1;31m 403\033[00m: {file_in_question} not found", 
        404: f'\033[1;31m 404\033[00m: {extra} not found', 200: f'\033[1;32m 200\033[00m: {extra} connected'}
        if status == 404:
            raise FileNotFoundError(report_cache[404])
        elif status == 403:
            raise FileNotFoundError(report_cache[403])
        else:
            print(report_cache[status])

    def base_case(self):
        sleep = 4
        self.__set_main_repo()
        print("\033[1;32m Connecting to data\033[00m")
        time.sleep(sleep)
        data_report, extra = self.__check_data_repo()
        self.__connection_checker(data_report, self.data_repo, extra)
        time.sleep(sleep)
        print("\033[1;32m Connecting to the machine learning models\033[00m")
        time.sleep(sleep)
        model_report, extra = self.__check_model_repo()
        time.sleep(sleep)
        self.__connection_checker(model_report, self.model_repo, extra)

        return {'model': model_report, 'data': data_report}

    def __set_main_repo(self):
        if not os.path.exists(self.repo):
            raise FileNotFoundError(f"\033[1;31m{path}\033[00m directory not found")
        
    def __check_data_repo(self) -> int:
        paths = ['/data.csv','/data_cleaned_v2.csv']
        if not os.path.exists(self.data_repo):
            return 403, self.data_repo

        for path in self.data_files:
            if not os.path.exists(self.data_repo + f'{path}'):
                return 404, self.data_repo + f'{path}'
            
        return 200, self.data_repo

    def __check_model_repo(self) -> [int,'str|Bool']:
        paths = ['./svd.pkl']
        if not os.path.exists(self.model_repo):
            return 403, self.model_repo

        for path in self.model_files:
            if not os.path.exists(self.model_repo + f'{path}'):
                return 404, self.model_repo + f'{path}'
            
        return 200, self.model_repo 


if __name__ == '__main__':
    basecase: BaseCase = BaseCase(r'E:/Internship')
    basecase.base_case()
    