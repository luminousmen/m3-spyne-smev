
from spyne_smev.client import Client
from soap11wsse import TEST_PRIVATE_KEY, TEST_X509_CERT


if __name__ == "__main__":
    client = Client(
        "http://localhost:8080?wsdl",
        private_key=TEST_PRIVATE_KEY, private_key_pass="12345678",
        certificate=TEST_X509_CERT)
    msg = client.factory.create("SayHello")
    msg.Message.Sender.Code = "Sndr12345"
    msg.Message.Sender.Name = "Sender"
    msg.Message.Recipient.Code = "Rcpnt1234"
    msg.Message.Recipient.Name = "Recipient"
    msg.MessageData.AppData.Name = "John Smith"
    msg.MessageData.AppData.Times = 5
    greetings = client.service.SayHello(
        msg.Message, msg.MessageData)
    if not client.last_verified:
        raise ValueError(
            "msg didn't pass validation checks. See debug log for details!")

    print("\n".join("{0}. {1}".format(i, name) for i, name in enumerate(
        greetings.MessageData.AppData.string)))
