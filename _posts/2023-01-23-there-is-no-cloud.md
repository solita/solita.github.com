# There Is No Cloud, It's Just Someone Else's Computer

This well-known adage unfortunately isn't a joke, and you should
clearly understand who actually owns (has access to all) your cloud
data. In most cases, no matter what you do, Big Brother easily
sees you encrypted cloud data in clear text. End of story. Why is
that? Because you routinely entrust encryption keys and certificate
management to the cloud. Remember Azure KeyVaults, AWS KMS, CloudHSM, 
GCP Cloud KMS, where you readily commit your most precious? All 
privacy is in private keys. Entrust not your goats to wolves.

Are there any solutions to this conundrum?

If you have lots of money and lawyers, you may try your chances in 
court trying to prevent your cloud providers from handing over your 
encryption keys to third parties, but there are cheaper and more 
reliable options.


## Client-Side Encryption Is Your Best Friend

The first obvious option is the so-called **client-side** encryption,
consisting in encrypting data on the client/sender side before
transmitting it to a server side such as a cloud storage service or
database. Client-side encryption uses an encryption key that is **not**
available to the service provider, making it impossible for service
provider to decrypt hosted data. Note that you keep your keys as well
as a client computer (e.g., your laptop) strictly out of the cloud;
otherwise your effort is immediately compromised.

Is client-side encryption mainstream? There are lots of open-source
cryptographic libraries you can use to encrypt your data before
submitting to a cloud, so you are all set. But can you 'transparently'
integrate client-side encryption with, say, cloud databases?
Transparently means you spend little or no effort on en/decrypting,
just do your usual database CRUD operations. Here we have quite a
limited choice.


## AWS

AWS offers DynamoDB Encryption Client in Java and Python only. You can
use these SDKs with AWS KMS (no real privacy) or provide your own
(full privacy) cryptographic material for encryption (you keep away
from the cloud). Unfortunately, at the time of writing, relational
databases in AWS lack client-side encryption support.


## Azure

How about Azure CosmosDB? They created the so-called Always Encrypted
client-side option for CosmosDB, in .NET and Java. Unfortunately, at
the time of writing, the only option to keep your customer-managed
keys CMK for client-side encryption (which should be your most
valuable private property) suggested by Microsoft is the Azure
KeyVault, which undermines the whole privacy idea (goats to wolves) 
straight away.


## Primary Keys Are NOT Encrypted

It is important to note that both AWS DynamoDB and Azure CosmosDB
require that you always leave the primary keys (partition/hash and
range/sort keys) **unencrypted**. The motivation is that NoSQL databases
need primary keys for proper and efficient storing and fetching data
(think of the necessity to repartition your DB when encryption keys
are rotated and encrypted primary keys change respectively). This
unencrypted primary keys requirement is necessary but a bit
disappointing, since it exposes part of your important data. If you
ever worked with NoSQL databases, you realize that normally primary
keys are composed of many other attributes to make searches efficient,
which exposes your data even more. For example, you may use name,
surname, and DOB as primary keys (some exposure) but use Bitcoin
credentials (extremely sensitive) for client-side encryption. 
Another example is you use a personal number as a(n unencrypted) 
primary key, but keep all other patient information fully client-side
encrypted. Full client-side encryption is of course possible if you 
store and operate your DB completely outside the cloud, then encrypt 
and upload it to the cloud. This is possible with the cloud blob 
storage in any cloud.


## GCP

In contrast to AWS and Azure, GCP offers client-side encryption for
Cloud SQL.


## Conclusions

Client-side encryption options are available, but not abundant. Let's 
expect more will emerge, since motivation is pretty obvious.


## References

https://docs.aws.amazon.com/dynamodb-encryption-client/latest/devguide/what-is-ddb-encrypt.html

https://learn.microsoft.com/en-us/azure/cosmos-db/how-to-always-encrypted

https://cloud.google.com/sql/docs/mysql/client-side-encryption

Just keep the key words "client side encryption in your Googling".


## Appendix: Python/AWS DynamoDB PoC Implementation


You start as usual:

```
session = boto3.Session(region_name=AWS_REGION)
client = session.resource('dynamodb')  # high-level client
table_name = 'test-table-1'
table = client.Table(table_name)  # existing EMPTY table
```

Then you give the Wrapped CMP, Cryptographic Material Provider, 
with an asymmetric key:

```
cmp = get_wrapped_cmp_asymm('key_asymm')  # my keys are in the files: key_asymm_wrap.bin and key_asymm_sign.bin
```

My utility CMP providing function (in another file) is:

```
def get_wrapped_cmp_asymm(key_name):
    key_file_wrap = f"{key_name}_wrap.bin"
    with open(key_file_wrap, 'rb') as f:
        rsa_wrapping_private_key_bytes = f.read()
    wrapping_key = JceNameLocalDelegatedKey(
        key=rsa_wrapping_private_key_bytes,
        algorithm="RSA",
        key_type=EncryptionKeyType.PRIVATE,
        key_encoding=KeyEncodingType.DER,
    )
    key_file_sign = f"{key_name}_sign.bin"
    with open(key_file_sign, 'rb') as f:
        rsa_signing_private_key_bytes = f.read()
    signing_key = JceNameLocalDelegatedKey(
        key=rsa_signing_private_key_bytes,
        algorithm="SHA512withRSA",
        key_type=EncryptionKeyType.PRIVATE,
        key_encoding=KeyEncodingType.DER,
    )
    wrapped_cmp = WrappedCryptographicMaterialsProvider(
        wrapping_key=wrapping_key, unwrapping_key=wrapping_key, signing_key=signing_key
    )
    return wrapped_cmp
```

Now, I define how to treat all attributes: by default, encrypt and sign every 
attribute (except private keys which are ALWAYS unencrypted); just for fun, I do 
not want to encrypt and sign the `test` attribute:

```
actions = AttributeActions(
    default_action=CryptoAction.ENCRYPT_AND_SIGN,
    attribute_actions={'test': CryptoAction.DO_NOTHING}
)
```

Next, I just WRAP my usual `table` as `EncryptedTable`, using `cmp` and `actions`:

```
encrypted_table = EncryptedTable(
    table=table,
    materials_provider=cmp,
    attribute_actions=actions
)
```

I am all set and can now add items to the `encrypted_table`, with the usual
`put_item` method:

```
plaintext_item_1 = {
    '0-pk': 'partition-value-01',
    '1-sk': '1',
    'example': 'data',
    'numbers': 99,
    'test': 'test-value'
}
encrypted_table.put_item(Item=plaintext_item_1)
```
Note that I put an **unencrypted** item which **transparently** gets encrypted 
using the `cmp` above, beforte being stored on AWS.

Similarly, I transparently get the unencrypted item using:

```
item = encrypted_table.get_item(Key={'0-pk': 'partition-value-01', '1-sk': '1'})
```

Let me reiterate that everything, namely `example` and `numbers` attributes 
on AWS is getting saved ENCRYPTED.

Let me show what you see on the AWS DynamoDB side:

```
{
  "0-pk": {
    "S": "partition-value-01"
  },
  "1-sk": {
    "S": "1"
  },
  "*amzn-ddb-map-desc*": {
    "B": "AAAAAAAAABBhbXpuLWRkYi1lbnYtYWxnAAAAB0FFUy8yNTYAAAAQYW16bi1kZGItZW52LWtleQAAADhaNUswVGxMV0JtS2VreDZwc0lOYlB0THphV0pxOGFlLytKNk9JMFVQVnhMNXk5Q1BLdG5RT1E9PQAAABdhbXpuLWRkYi1tYXAtc2lnbmluZ0FsZwAAAApIbWFjU0hBNTEyAAAAFWFtem4tZGRiLW1hcC1zeW0tbW9kZQAAABEvQ0JDL1BLQ1M1UGFkZGluZwAAABFhbXpuLWRkYi13cmFwLWFsZwAAAAdBRVNXcmFw"
  },
  "*amzn-ddb-map-sig*": {
    "B": "3AZffQmyNl0w7QcznfBvCy2TfRmyNfOqnITu1hrO/JDc2M1hAL01E0yqIJSgFtkISIk5TtXdaZoXAfOjN6jHiw=="
  },
  "example": {
    "B": "ITFfW5lICGQIoK29WvZoh0cmwaKteDack3KmgXBZxCo="
  },
  "numbers": {
    "B": "kgPie2XmokAps6XDKx3KwHQEkq0AtlfhoqT8joSQ6xE="
  },
  "test": {
    "S": "test-value"
  }
}
```
First off, you see the partition `0-pk` and sort `1-sk` keys UNENCRYPTED.
Second, remember that the `test` attribute was UNENCRYPTED for fun.
Third, most importantly, all other attributes, namely, `example` and `numbres` 
are duly ENCRYPTED! We also see a few of service `*amzn` fields, which
describe encryption.

All right, I revealed everything except how I created my DynamoDB table:

```
table = client.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': '0-pk',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': '1-sk',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': '0-pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': '1-sk',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
```
Here I just define my primary (partition/hash + sort/range) keys, 
NoSQL business as usual.

And the last most important thing - here is how I generate my wrapping and 
signing keys, ON PREMISES, and never give them away:

```
def create_asymmetric_keys():
    wrapping_key_bytes = JceNameLocalDelegatedKey.generate("RSA", 4096).key
    signing_key_bytes = JceNameLocalDelegatedKey.generate("SHA512withRSA", 4096).key
    file_name = 'key_asymm_wrap.bin'
    with open(file_name, 'wb') as f:
        f.write(wrapping_key_bytes)
    os.chmod(file_name, 0o600)
    file_name = 'key_asymm_sign.bin'
    with open(file_name, 'wb') as f:
        f.write(signing_key_bytes)
    os.chmod(file_name, 0o600)
```
This is as simple as possible, for PoC, because in production you need to 
organize for a proper PKI. Similarly, you may use symmetric keys if you want.


## That's All, Folks!

## Or Not?

## Your Next Friend is FHE - Fully Homomorphic Encryption

Stay tuned.
