Search.setIndex({docnames:["backends","django","index","install","modules","preauth","refund","usage","web_payments","web_payments.django","web_payments_dummy","web_payments_externalpayments"],envversion:53,filenames:["backends.rst","django.rst","index.rst","install.rst","modules.rst","preauth.rst","refund.rst","usage.rst","web_payments.rst","web_payments.django.rst","web_payments_dummy.rst","web_payments_externalpayments.rst"],objects:{"":{web_payments:[8,0,0,"-"],web_payments_dummy:[10,0,0,"-"],web_payments_externalpayments:[11,0,0,"-"]},"web_payments.FraudStatus":{ACCEPT:[8,3,1,""],CHOICES:[8,3,1,""],REJECT:[8,3,1,""],REVIEW:[8,3,1,""],UNKNOWN:[8,3,1,""]},"web_payments.HttpRequest":{GET:[8,3,1,""],POST:[8,3,1,""],content_type:[8,3,1,""],method:[8,3,1,""]},"web_payments.PaymentStatus":{CHOICES:[8,3,1,""],CONFIRMED:[8,3,1,""],ERROR:[8,3,1,""],INPUT:[8,3,1,""],PREAUTH:[8,3,1,""],REFUNDED:[8,3,1,""],REJECTED:[8,3,1,""],WAITING:[8,3,1,""]},"web_payments.PurchasedItem":{currency:[8,3,1,""],name:[8,3,1,""],price:[8,3,1,""],quantity:[8,3,1,""],sku:[8,3,1,""]},"web_payments.django":{apps:[9,0,0,"-"],get_base_url:[9,5,1,""],get_payment_model:[9,5,1,""],initialize:[9,5,1,""],models:[9,0,0,"-"],signals:[9,0,0,"-"],urls:[9,0,0,"-"]},"web_payments.django.apps":{WebPaymentsConfig:[9,2,1,""]},"web_payments.django.apps.WebPaymentsConfig":{name:[9,3,1,""],ready:[9,4,1,""]},"web_payments.django.models":{BasePayment:[9,2,1,""],BasePaymentWithAddress:[9,2,1,""]},"web_payments.django.models.BasePayment":{Meta:[9,2,1,""],check_token_exists:[9,6,1,""],get_fraud_status_display:[9,4,1,""],get_process_url:[9,4,1,""],get_provider_variant:[9,4,1,""],get_status_display:[9,4,1,""],list_providers:[9,6,1,""],save:[9,4,1,""],signal_status_change:[9,4,1,""]},"web_payments.django.models.BasePayment.Meta":{"abstract":[9,3,1,""]},"web_payments.django.models.BasePaymentWithAddress":{Meta:[9,2,1,""],billing_address_1:[9,3,1,""],billing_address_2:[9,3,1,""],billing_city:[9,3,1,""],billing_country_area:[9,3,1,""],billing_country_code:[9,3,1,""],billing_email:[9,3,1,""],billing_first_name:[9,3,1,""],billing_last_name:[9,3,1,""],billing_postcode:[9,3,1,""],get_billing_address:[9,4,1,""],get_fraud_status_display:[9,4,1,""],get_shipping_address:[9,4,1,""],get_status_display:[9,4,1,""]},"web_payments.django.models.BasePaymentWithAddress.Meta":{"abstract":[9,3,1,""]},"web_payments.django.urls":{process_data:[9,5,1,""],static_callback:[9,5,1,""]},"web_payments.forms":{CreditCardNumberValidator:[8,2,1,""],CreditCardPaymentForm:[8,2,1,""],CreditCardPaymentFormWithName:[8,2,1,""],DateValidator:[8,2,1,""],PaymentForm:[8,2,1,""]},"web_payments.forms.CreditCardNumberValidator":{cart_number_checksum_validation:[8,7,1,""]},"web_payments.forms.CreditCardPaymentForm":{VALID_TYPES:[8,3,1,""],cvv2:[8,3,1,""],expiration:[8,3,1,""],number:[8,3,1,""],validate_number:[8,4,1,""]},"web_payments.forms.CreditCardPaymentFormWithName":{name:[8,3,1,""]},"web_payments.forms.PaymentForm":{Meta:[8,2,1,""],action:[8,3,1,""],method:[8,3,1,""],payment:[8,3,1,""],provider:[8,3,1,""]},"web_payments.forms.PaymentForm.Meta":{wrap_formdata:[8,4,1,""]},"web_payments.logic":{BasicPayment:[8,2,1,""],BasicProvider:[8,2,1,""]},"web_payments.logic.BasicPayment":{attrs:[8,3,1,""],capture:[8,4,1,""],captured_amount:[8,3,1,""],change_fraud_status:[8,4,1,""],change_status:[8,4,1,""],check_token_exists:[8,6,1,""],create_token:[8,4,1,""],currency:[8,3,1,""],extra_data:[8,3,1,""],fraud_message:[8,3,1,""],fraud_status:[8,3,1,""],get_billing_address:[8,4,1,""],get_failure_url:[8,4,1,""],get_form:[8,4,1,""],get_payment_extra:[8,4,1,""],get_process_url:[8,4,1,""],get_provider_variant:[8,4,1,""],get_purchased_items:[8,4,1,""],get_shipping_address:[8,4,1,""],get_success_url:[8,4,1,""],list_providers:[8,6,1,""],load_providers:[8,6,1,""],message:[8,3,1,""],provider:[8,3,1,""],refund:[8,4,1,""],release:[8,4,1,""],save:[8,4,1,""],signal_status_change:[8,4,1,""],status:[8,3,1,""],token:[8,3,1,""],total:[8,3,1,""],transaction_id:[8,3,1,""],variant:[8,3,1,""]},"web_payments.logic.BasicProvider":{capture:[8,4,1,""],clear_token_cache:[8,4,1,""],extra:[8,3,1,""],form_class:[8,3,1,""],get_action:[8,4,1,""],get_auth_token:[8,4,1,""],get_form:[8,4,1,""],get_token_from_request:[8,4,1,""],process_data:[8,4,1,""],refund:[8,4,1,""],release:[8,4,1,""],token:[8,3,1,""]},"web_payments.testcommon":{create_test_payment:[8,5,1,""]},"web_payments.translation":{Translation:[8,2,1,""],get_language:[8,5,1,""],set_language:[8,5,1,""]},"web_payments.translation.Translation":{domain:[8,3,1,""],fallback:[8,3,1,""],gettext:[8,4,1,""],gettext_lazy:[8,4,1,""],instance_path:[8,3,1,""],ngettext:[8,4,1,""],ngettext_lazy:[8,4,1,""],trans:[8,4,1,""],translation_path:[8,3,1,""]},"web_payments.utils":{get_credit_card_issuer:[8,5,1,""],getter_prefixed_address:[8,5,1,""],split_streetnr:[8,5,1,""]},"web_payments_dummy.DummyProvider":{capture:[10,4,1,""],extra:[10,3,1,""],get_auth_token:[10,4,1,""],get_form:[10,4,1,""],process_data:[10,4,1,""],refund:[10,4,1,""],release:[10,4,1,""]},"web_payments_dummy.forms":{DummyForm:[10,2,1,""]},"web_payments_dummy.forms.DummyForm":{RESPONSE_CHOICES:[10,3,1,""],fraud_status:[10,3,1,""],gateway_response:[10,3,1,""],status:[10,3,1,""],validate:[10,4,1,""],verification_result:[10,3,1,""]},"web_payments_externalpayments.BankTransferProvider":{get_fields:[11,4,1,""],get_form:[11,4,1,""],refund:[11,4,1,""]},"web_payments_externalpayments.DirectPaymentProvider":{get_form:[11,4,1,""],refund:[11,4,1,""]},"web_payments_externalpayments.forms":{IBANBankingForm:[11,2,1,""],OrderIdForm:[11,2,1,""]},"web_payments_externalpayments.forms.IBANBankingForm":{bic:[11,3,1,""],iban:[11,3,1,""],order:[11,3,1,""]},"web_payments_externalpayments.forms.OrderIdForm":{order:[11,3,1,""]},web_payments:{ExternalPostNeeded:[8,1,1,""],FraudStatus:[8,2,1,""],HttpRequest:[8,2,1,""],NotInitialized:[8,1,1,""],NotSupported:[8,1,1,""],PaymentError:[8,1,1,""],PaymentStatus:[8,2,1,""],PurchasedItem:[8,2,1,""],RedirectNeeded:[8,1,1,""],django:[9,0,0,"-"],forms:[8,0,0,"-"],logic:[8,0,0,"-"],provider_factory:[8,5,1,""],status:[8,0,0,"-"],testcommon:[8,0,0,"-"],translation:[8,0,0,"-"],utils:[8,0,0,"-"]},web_payments_dummy:{DummyProvider:[10,2,1,""],forms:[10,0,0,"-"]},web_payments_externalpayments:{BankTransferProvider:[11,2,1,""],DirectPaymentProvider:[11,2,1,""],forms:[11,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","exception","Python exception"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"],"5":["py","function","Python function"],"6":["py","classmethod","Python class method"],"7":["py","staticmethod","Python static method"]},objtypes:{"0":"py:module","1":"py:exception","2":"py:class","3":"py:attribute","4":"py:method","5":"py:function","6":"py:classmethod","7":"py:staticmethod"},terms:{"221b":7,"3DS":10,"3ds":10,"6xe":7,"abstract":9,"class":[0,1,3,8,9,10,11],"default":[1,2,5,6,7,8,10,11],"final":[5,7,8,10],"function":8,"import":[1,3,5,6,7],"new":8,"return":[1,3,8,9,10,11],"static":8,"true":[0,3,5,8,10,11],"try":[1,3],"void":5,Adding:0,For:[0,8],Has:9,The:[1,3,7,9,11],Use:8,_kwarg:8,accept:[7,8,10],access:[7,8],accord:9,action:[3,8],activ:9,actual:7,add:[8,11],address:[8,9],address_1:3,address_2:3,affect:0,after:[5,7],age:8,alia:[8,9],all:8,allow:[5,11],also:[1,8],alwai:8,american:8,amount:[2,5,6,8,10,11],ani:10,annil:[8,10],api:8,app:[4,8],app_modul:9,app_nam:9,appconfig:9,appear:7,applic:8,appropri:9,arg:[1,3,9],argument:[2,8,10],around:8,ascii:1,assign:7,associ:1,asynchron:9,attr:8,attribut:8,authent:[8,10],author:[2,7,8,10],autocomplet:8,automat:[8,9],back:8,backend:[2,5,8,9],baker:7,bank:[3,11],banktransferprovid:[8,11],base:[8,9,10,11],basepay:[1,9],basepaymentwithaddress:[1,9],bash:0,basi:8,basic:2,basicpay:[3,8,9],basicprovid:[8,10,11],baskervil:[1,3],becaus:11,been:7,behind:0,best:1,bic:[8,11],bill:[8,9],billing_address_1:[7,9],billing_address_2:[7,9],billing_c:[7,9],billing_country_area:[7,9],billing_country_cod:[7,9],billing_email:9,billing_first_nam:[7,9],billing_last_nam:[7,9],billing_postcod:[7,9],block:0,book:7,bool:[8,11],bskv:[1,3],builtin:2,buyer:5,cach:[0,8,10],call:[5,6,8,9,10],callabl:[1,9],callback:[1,8,9,10],can:[0,1,3,5,6,7,8,9,10,11],captur:[0,2,3,7,8,10],captured_amount:[5,7,8],card:8,cart_number_checksum_valid:8,cash:11,chang:[8,9],change_fraud_statu:8,change_statu:8,charact:11,charfield:9,charg:7,check:[7,8,9],check_token_exist:[8,9],choic:[8,10],chosen:9,citi:3,classmethod:[3,8,9],clear:8,clear_token_cach:8,cls:3,code:[0,8,9],collect:5,com:[1,3],commit:8,commun:[7,8,9],complet:11,config:9,configur:[1,5],confirm:[6,7,8,10,11],connect:10,connector:3,content:[2,4,7],content_typ:8,control:9,convert:[8,10,11],cost:8,country_area:3,country_cod:3,creat:[1,3,7,8,9],create_test_pay:8,create_token:8,credit:8,creditcardnumbervalid:8,creditcardpaymentform:8,creditcardpaymentformwithnam:8,csc:8,cur_lang:8,currenc:[1,3,7,8],current:[7,8,9],custom:[7,8,9],cvv2:8,dabaie2d:8,data:[1,3,7,8,9,10,11],date:8,datefield:8,datetim:[8,10],datevalid:8,decim:[1,3,5,6,7,8],def:[1,3],default2:1,defer:9,defin:8,definit:2,deliveri:[3,7,8,11],depend:8,descript:[7,8],detail:7,detect:7,develop:0,dict:8,dictionari:0,differ:[0,8],digit:8,directli:8,directpaymentprovid:[8,11],disabl:[8,10],displai:8,django:[0,2,3,4,8],django_dummi:0,django_settings_modul:0,doe:9,doesn:11,domain:[8,9],don:11,done:[0,11],dummi:10,dummyform:10,dummyprovid:[1,5,8,10],dure:7,each:[9,10],els:11,email:3,enabl:[0,5],endfor:3,environ:0,equival:9,error:[3,7,8,10],everi:11,exampl:[0,1,3,8,9],except:[0,1,3,8,9],execut:9,exist:[0,9],exp:8,expir:[8,10],express:8,extend:8,externalpay:0,externalpostneed:8,extra:[1,2,8,10],extra_data:[7,8,9],extra_stuff:3,extract:8,face:3,failur:[1,3,10],fallback:8,fals:[0,5,7,8,9,11],fanci:1,field:[3,7,8,9,10],fieldnam:10,first:[7,9],first_nam:3,flag:7,folder:0,force_insert:9,force_upd:9,form:[1,3,4,7],form_class:8,format:8,formdata:8,found:8,four:8,fraction:[8,10],fraud:[2,8],fraud_messag:[7,8],fraud_statu:[7,8,9,10],fraudstatu:8,from:[0,1,3,5,6,7,8,9,10],front:8,full:1,func:3,fund:7,further:11,gatewai:[5,7,10],gateway_messag:8,gateway_respons:10,get:[1,5,6,8,9],get_act:8,get_auth_token:[8,10],get_base_url:9,get_billing_address:[3,8,9],get_credit_card_issu:8,get_failure_url:[1,3,8],get_field:11,get_form:[1,3,8,10,11],get_fraud_status_displai:9,get_languag:8,get_object_or_404:1,get_payment_extra:[3,8],get_payment_model:[1,9],get_process_url:[3,8,9],get_provider_vari:[3,8,9],get_purchased_item:[1,3,8],get_shipping_address:[3,8,9],get_status_displai:9,get_success_url:[1,3,8],get_token_from_request:8,getter:8,getter_prefixed_address:8,gettext:8,gettext_lazi:8,gitignor:0,gl5604449876543210:8,good:0,greater:7,gross:8,had:8,handl:3,has:[5,7,9,11],have:[0,5,7],helper:2,hold:11,holm:7,host:9,hound:[1,3],how:0,html:[1,3],http404:9,http:[1,3],httprequest:8,human:11,iban:[8,11],ibanbankingform:11,icon:1,implement:8,includ:1,index:2,indic:7,inform:1,inherit:0,initi:[8,9],input:[3,7,8,10],inputrequir:[8,10],insert:9,insist:9,inspect:7,instal:2,installed_app:1,instanc:[1,3,5,6,7,8,9],instance_path:8,instanti:8,instead:8,integr:0,involv:7,is_dummi:10,iter:[1,3,8,9],its:7,john:3,johnstreet:3,just:11,kei:0,kept:[8,9],keyword:8,known:5,kwarg:[3,8,9,10,11],label:[3,8,11],languag:[8,9],last:8,last_nam:3,least:0,left:[0,8],length:8,let:7,like:8,list:8,list_provid:[3,8,9],live:0,load:[8,9],load_provid:8,localhost:1,localized_nam:[1,8],locat:[0,8],logic:[3,4,9,10,11],london:7,longer:11,lower:5,mai:[1,3,7,8],make:2,manag:0,mani:[0,11],manual:[5,11],mark:7,messag:[7,8],meta:[8,9],method:[1,3,5,6,8,9],minimum:8,minimumag:8,model:[1,3,4,8],modul:[2,4],more:[1,9],msg:8,msgplural:8,much:11,multipl:5,must:[8,9,10],mybackend:3,mypaymentapp:[1,3],name:[0,1,3,8,9,11],nech:3,need:6,next:3,ngettext:8,ngettext_lazi:8,non:9,none:[1,3,8,9,10,11],normal:9,notabl:0,note:[1,3,8],notimpl:8,notimplementederror:8,notiniti:8,notsupport:8,now:[7,8,10],number:[8,11],nw1:7,object:[1,5,6,7,8,9,10],obtain:3,occur:7,off:11,offer:5,offici:8,one:[7,8,9],onli:[0,5,6,7,11],oper:11,option:3,order:[1,11],orderidform:11,other:11,otherwis:9,overrid:9,overwrit:[8,9],overwritten:[8,9],own:0,packag:[0,2,4],page:2,pai:11,pair:1,param:[],paramet:[0,5,6,8,9,11],partial:6,pass:[3,7,8,10],pattern:8,payment:[1,3,8,9,10,11],payment_detail:1,payment_host:[1,9],payment_id:1,payment_model:1,payment_protocol:[1,9],payment_variants_api:[1,5,7,8],paymenterror:8,paymentform:[8,10,11],paymentitem:9,paymentstatu:[8,11],paymentvari:5,peopl:11,perform:6,physic:8,pip:3,placehold:11,pleas:[1,3,7,11],png:1,point:0,possibl:[7,8],post:[1,3,8],postcod:3,pre:[8,10],preauth:[0,5,7,8,10],prefix:[8,11],price:[1,3,8],probabl:1,problem:[7,11],proce:3,process:[3,8,9,10],process_data:[8,9,10],process_url:[8,9],processor:1,project:[2,9],protocol:9,provid:[0,1,3,5,6,7,8,9,10,11],provider_factori:[0,8],providervari:[1,3,8,9],pseudo:8,purchas:7,purchaseditem:[1,3,8],pythonpath:3,quantiti:[1,3,8],queri:9,rais:[1,3,9],ration:0,read:9,readi:9,readonli:11,real:9,redirect:[1,3,8,10],redirect_to:[1,3],redirectneed:[1,3,8],refer:11,refund:[2,7,8,10,11],refunded_amount:6,regexp:8,reject:[7,8,10],releas:[2,8,10],rememb:[7,8],render:3,render_kw:[8,11],repres:9,request:[1,3,7,8,9,10],requir:[3,8,11],respect:9,respons:[1,7,9,10],response_choic:10,restaur:11,result:9,retriev:1,review:[7,8,10],run:[0,9],runserv:0,same:0,save:[8,9],search:2,second:0,secret:[8,9],secur:[8,11],see:[0,3,7,8,9],select:8,selectfield:10,self:[1,3],send:[8,9,11],server:0,servic:7,set:[0,1,5,7,8,9,11],set_languag:8,sever:7,sherlock:7,ship:8,shippingaddress:9,shortcut:1,should:[0,1,3,8,9],show:11,side:8,signal:[4,8],signal_status_chang:[8,9],singl:9,site:9,skipform:11,sku:[1,3,8],smith:3,softwar:11,some:[5,7],somebodi:[8,10,11],sophist:1,sourc:[8,9,10,11],specif:8,specifi:9,split_streetnr:8,sql:9,start:9,state:7,static_callback:[8,9],statu:[4,5,6,7,9,10],status:2,status_chang:8,step:[3,5],stick:1,store:7,str:[8,11],street:7,stringfield:[8,11],subclass:[1,3,9],submit:3,submodul:4,subpackag:4,success:[1,3,8],successfulli:7,suppli:11,support:8,take:[1,5,8,10],tax:[3,7,8],templat:[1,3],templaterespons:1,tennesse:3,test:[2,8],test_var:8,testcommon:[0,3,4],thei:9,thi:[0,5,6,7,8,9],three:8,time:[0,8,9],time_reserv:[0,8,10],timedelta:[0,8,10],timezon:[8,10],token:[0,3,8,9,10,11],total:[5,6,7,8,10],tran:8,transact:[5,8,9,11],transaction_id:8,translat:4,translation_path:8,treat:9,tri:[8,10],tupl:8,two:[5,7],type:[0,3,5,8],unboundfield:[8,10,11],univers:8,unknown:[7,8,10],unsupport:10,until:8,updat:[8,9],url:[1,3,4,8],urlpattern:1,usd:[1,3,7],use:[1,8,11],used:[0,1,7,8,9,11],useful:[8,9],user:11,usetoken:11,using:7,utc:[8,10],util:4,valid:[8,10],valid_typ:8,validate_:10,validate_numb:8,valu:[3,8,9],variabl:[0,9],variant:[1,7,8,9],variantnam:8,verifi:11,verification_result:10,view:[1,3],voucher:11,wait:[7,8,10],want:[1,9],web:3,web_pay:[1,2,3,10,11],web_payments_dummi:[0,1,2,4,5,8],web_payments_externalpay:[0,2,4,8],webpaymentsconfig:9,were:7,what:8,when:[7,8,9,10,11],where:8,which:[1,5,7,8,10,11],work:8,would:6,wrap_formdata:8,wrapper:9,write:[2,3],wtform:[8,10],yield:[1,3],you:[1,3,5,6,7,9,11],your:[0,5,6,7,8],yyyi:8,zero:8},titles:["Basic Backend Definition","Django Helpers","Welcome to web-payments-connector\u2019s documentation!","Installation","web_payments","Authorization and capture","Refunding a payment","Making a payment","web_payments package","web_payments.django package","web_payments_dummy package","web_payments_externalpayments package"],titleterms:{"default":0,amount:7,app:9,argument:0,author:5,backend:0,basic:0,builtin:0,captur:5,connector:2,content:[8,9,10,11],definit:0,django:[1,9],document:2,extra:0,form:[8,10,11],fraud:7,helper:1,indic:2,instal:3,logic:8,make:7,model:9,modul:[8,9,10,11],packag:[8,9,10,11],payment:[2,5,6,7],project:0,refund:6,releas:5,signal:9,statu:8,status:7,submodul:[8,9,10,11],subpackag:8,tabl:2,test:0,testcommon:8,translat:8,url:9,util:8,web:2,web_pay:[4,8,9],web_payments_dummi:10,web_payments_externalpay:11,welcom:2,write:0}})