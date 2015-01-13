from qiniu import Auth
#from mysite import settings
AccessKey='PS9Yw-2b8qL6PihR2h5pSmow7Z1Hh3s35LVPnPZM'
SecretKey='Tm9qUpMQ92a2eaEfbtqhaYE9tMBR_GMAkr22UEQa'
csrfName='csrfmiddlewaretoken'
callbackUrl="http://ncwugirl.duapp.com/girl/qncallback/"
callbackBody="name=$(key)&bucket=$(bucket)&mimeType=$(mimeType)&desc=$(x:desc)&csrfmiddlewaretoken=$(x:csrfmiddlewaretoken)"
policy={'callbackUrl':callbackUrl,'callbackBody':callbackBody}
def getToken():
    q=Auth(AccessKey,SecretKey)
    token=q.upload_token(bucket='ncwugirl',policy=policy)
    return token
