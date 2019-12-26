from RBAC.models import Company
import csv


def csv_reader(csvFile):
    with open(csvFile.name, 'r', encoding='UTF-8')as f:
        f_csv = csv.reader(f)
        for i, line in enumerate(f_csv):
            if i == 0:
                continue
            company_key = line[1]
            company_obj = Company.objects.get_or_create(key=company_key)
            company_obj = company_obj[0]
            company_obj.name = line[0]
            company_obj.address = line[2]
            company_obj.web = line[3]
            company_obj.manage = line[4]
            company_obj.idcard = line[5]
            company_obj.mobilephone = line[6]
            company_obj.teamname = line[7]
            company_obj.teamaddress = line[8]
            company_obj.save()
