# README
* * *

## ABOUT

spyne-smev - это набор протоколов фреймворка [spyne](http://spyne.io/>)
для работы с системой межведомственного электронного взаимодействия или просто
[СМЭВ](http://smev.gosuslugi.ru/>).


## REQUIREMENTS

* lxml (манипуляции с xml документами)
* cryptography (биндинг к libssl)
* spyne (необходим для работы протоколов spyne)
* suds (необходим только для работы клиента suds)


## INSTALLATION

1. Сперва необходимо установить openssl и все сопутствующие ему библиотеки.
   Для различных операционных систем способ установки будет отличаться.

   Установка на Ubuntu:

    $ sudo apt-get install openssl libssl1.0.0 libssl-dev


2. Установка библиотеки:

    $ pip install https://bitbucket.org/barsgroup/spyne-smev/get/tip.tar.gz


## Использование

Модуль предоставляет набор классов расширяющих возможности базового протокола
фреймворка spyne - `Soap11`.

### WS-Security

`Soap11Wsse` - базовый протокол. Расширяет класс `Soap11`.
Добавляет в него функционал позволяющий применить некий профиль безопасности
к исходящему сообщению, и выполнить валидацию входящего в соответсвии с
этим профилем. Эти действия делегируются классу-наследнику
`BaseWSSProfile`, который соответственно должен реализовать два метода:
`apply` и `verify`.

`X509TokenProfile`, профиль который реализует механизм подписи
[XMLDSIG](http://www.w3.org/TR/xmldsig-core) по спецификации
[x509 token profile](http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0.pdf)

Пример создания django view для сервиса с применением подписи XMLDSIG:

    from spyne.application import Application
    from spyne.server.django import DjangoApplication

    from spyne_smev.wsse.protocols import Soap11WSSE, X509TokenProfile

    in_security = X509TokenProfile(
        private_key=in_private_key,
        private_key_pass=in_password,
        certificate=in_certificate,
        digest_method="sha1")
    in_protocol = Soap11WSSE(wsse_security=in_security)
    out_security = X509TokenProfile(
        private_key=out_private_key,
        private_key_pass=out_password,
        certificate=out_certificate,
        digest_method="sha1")
    out_protocol = Soap11WSSE(wsse_security=out_security)

    application = Application(
        [MyServiceBase], "http://my-domain.site/tns",
        in_protocol=in_protocol,
        out_protocol=out_protocol)
    service_view = DjangoApplication(application)


### СМЭВ

По [методическим рекомендациям](http://smev.gosuslugi.ru/portal/api/files/get/27403)
СМЭВ все сообщения должны быть подписаны электронной подписью.

Пример:

    from spyne.application import Application
    from spyne.server.django import DjangoApplication

    from spyne_smev.smev256 import Smev256
    from spyne_smev.wsse.protocols import X509TokenProfile

    in_security = X509TokenProfile(
        private_key=in_private_key,
        private_key_pass=in_password,
        certificate=in_certificate,
        digest_method="md_gost94")
    out_security = X509TokenProfile(
        private_key=out_private_key,
        private_key_pass=out_password,
        certificate=out_certificate,
        digest_method="md_gost94")

    in_protocol = Smev256(wsse_security=in_security)
    out_protocol = Smev256(
        wsse_security=out_security,
        SenderCode="123456789",
        SenderName="EDUPORTAL",
        RecipientCode="987654321",
        RecipientName="GOVPORTAL",
        Mnemonic="123456789",
        Version="1.00")


### Клиент

В качестве клиента используется suds с небольшими дополнениями, речь о которых
пойдет дальше. О том как устроен и работает suds можно почитать в официальной
документации к [suds](link_to_suds_documentation).

В классе `spyne_smev.client.Client` запрещено форматирование `prettyxml`,
а так же добавлен плагин подписи и верификации сообщений, работающий аналогично
профилю `X509TokenProfile`.

Пример:


## LIMITATIONS

* Поддерживается только протокол СМЭВ версии 2.5.6
* Пока не поддерживаются ссылки на вложения в AppDocument, а так же не
  реализовано api для упаковки файлов в BinaryData согласно рекомендациям
  (пока все делаем ручками)
* Клиент для подписи и верификации использует один сертификат (скорее это бага)

## LICENCE