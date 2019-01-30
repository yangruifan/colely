import pymysql
import  pandas as pd
import  time
import  numpy as np


class Operate_datebase_table(object):

    def __init__(self,table_name):
            connect = pymysql.Connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='960823',
                db='scrapy',
                charset='utf8',
                autocommit=True
            )
            self.cursor = connect.cursor()
            self.table_name=table_name

    def insertTable(self,field_name,data_tuple):
        '''

        :param field_name: 字段名,something like:(title,author..)
        :param data_tuple: something like:((1,2),(3,4),(5,6),(7,8)......) or (1,2)
        :param condition(default:none):
        :return: None
        '''
        # equals to insert into table_name(title,author) values (1,2),(3,4),(5,6)....
        #how to use it? like  c.insertTable('(content_token,url_token,contents)',((1,2,3),(4,5,6)))
        insert_data=','.join([str(s) for s in data_tuple])
        sql="insert into {0}{1} values {2}".format(self.table_name,str(field_name),insert_data)

        self.cursor.execute(sql)
        print("=========================>{}<==================================\n".format(time.strftime("%Y%m%d %H:%M:%S")))
        print("insert datas into table {} sucessfully".format(self.table_name))

    def deleteFromTable(self,condition=None):
        '''

        :param condition:something like: "id=3","id>1 and id<6".....必须要写为字符串形式
        :return: none
        '''
        #equals to delete from table_name where id=3
        # how to use it? like  deleteFromTable("id=3")

        if condition==None:
            raise Exception('your current operation is dangerous!\ncancelled automatically')
        delete_sql="delete from {0} where {1}".format(self.table_name,condition)
        self.cursor.execute(delete_sql)
        print("=========================>{}<==================================\n".format(time.strftime("%Y%m%d %H:%M:%S")))
        print("delete datas which meet the condition({0}) from {1} sucessfully".format(condition,self.table_name))


    def updateTale(self,map,condition=None):
        '''

        :param map: something like {'title':'obb','source':'shiguang'....}
        :param condition: something like   id=3 or source='时光网' or...
        :return:none
        '''
        #  equals to: update table_name set title='obb',source='shiguang'.... where condition
        if condition==None:
            raise Exception('your current updating operation is lack of condition')
        if '>' in condition or '<' in condition:
            raise  Exception("conditions can not contains '>,<',mustbe = ")
        update_sql="update {0} set ".format(self.table_name)
        for key,value in map.items():
            if(value.isdigit()):
                update_sql+=str(key)+'='+str(value)+','
            else:
                update_sql += str(key) + "=\'" + str(value) +"\'"+','
        update_sql=update_sql[:-1]+" where {}".format(condition)

        self.cursor.execute(update_sql)
        print("=========================>{}<==================================\n".format(time.strftime("%Y%m%d %H:%M:%S")))
        print("sucefucelly updates data")

    def updataMany(self,field_name,data_tuple):
        '''

        :param field_name: 字段名,something like:(title,author..)
        :param data_tuple: something like:((1,2),(3,4),(5,6),(7,8)......) or (1,2)
        :return: none
        '''
        '''
        此方法:
        1.适用于大批量更新数据库，例如要更新之前爬过的文章内容或者链接
        2.适用于只更新重复索引值所在一行的指定字段的值
        必须要加唯一索引！！！！！(索引可以为详情页url的md5,必须保证在表里是唯一的)
       
        '''
        field_list=field_name[1:-1].split(',')
        field_assignment=''
        for field in field_list:
            field_assignment+=str(field)+'=VALUES({})'.format(str(field))+','
        field_assignment=field_assignment[:-1]
        insert_data = ','.join([str(s) for s in data_tuple])
        sql="insert into {0}{1} values {2} ON DUPLICATE KEY UPDATE {3}".format(self.table_name,str(field_name),insert_data,field_assignment)
        self.cursor.execute(sql)
        print("=========================>{}<==================================\n".format(time.strftime("%Y%m%d %H:%M:%S")))
        print("update successfully!")



    def selectTable(self,field_name,condition=None):
        '''

        :param field_name: 字段名,something like:(title,author..)
        :param condition: something like that "id=3" ..."id < 3 limit 1"...."group by title limit 1"
        :return: something like (('','',''),('','',''))

        '''
        '''
        注意返回格式为   (('','',''),('','',''))  ，仅仅展示为dataframe
        '''
        field_name=field_name[1:-1]
        if condition !=None:
            if 'Group by' and 'group by' not in str(condition):
                 sql="select {0} from {1} where {2}".format(field_name,self.table_name,str(condition))
            else:
                sql = "select {0} from {1} {2}".format(field_name, self.table_name, str(condition))
        else:
            sql = "select {0} from {1}".format(field_name, self.table_name)
        self.cursor.execute(sql)
        select_data=self.cursor.fetchall()
        numpy_data=np.array(select_data)
        try:
            data=pd.DataFrame(data=numpy_data,columns=field_name.split(','))
        except:
            data=()
        print("=========================>{}<==================================\n".format(time.strftime("%Y%m%d %H:%M:%S")))
        print("查询结果：\n",data)
        return  select_data