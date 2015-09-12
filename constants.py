import os

PRODUCTION_MODE = True

if os.environ.get('OPENSHIFT_MYSQL_DB_URL') is None:
	MYSQL_URI = 'mysql://root:@localhost/timetables'
else:
	MYSQL_URI = os.environ['OPENSHIFT_MYSQL_DB_URL']+os.environ['OPENSHIFT_APP_NAME']


# if os.environ.get('OPENSHIFT_REPO_DIR') is None:
# 	if PRODUCTION_MODE:
# 		APNS_CERT = 'ck.pem'
# 	else:
# 		APNS_CERT = 'ck_dev.pem'
# else:
# 	if PRODUCTION_MODE:
# 		APNS_CERT = os.environ['OPENSHIFT_REPO_DIR']+'ck.pem'
# 	else:
# 		APNS_CERT = os.environ['OPENSHIFT_REPO_DIR']+'ck_dev.pem'
