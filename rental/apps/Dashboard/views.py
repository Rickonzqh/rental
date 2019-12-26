#coding:utf-8
from AssetManage import models as assetmodels

# Create your views here.


def getallcount(request):
    user = request.user
    data = {
      "code": 0,
      "msg": "",
      "count": '',
      "data": {
          'rootasset_count':0,
          'asset_count':0,
          'task_count':0,
          'vuln_count':0,
          'evaluation_count':0
          }
    }
    rootasset_count = assetmodels.Asset.objects.filter(is_root=True,user=user).count()
    asset_count = assetmodels.Asset.objects.filter(is_root=False,user=user).count()
    pass