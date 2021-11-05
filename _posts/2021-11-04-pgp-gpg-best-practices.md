---
layout: post
title: Supply chain is the new y2k. PGP USB HSM best practices for developers
date: 2016-11-04 17:49:22 +0200
author: kivilahtio
excerpt: > 
  "It is estimated that there will be four times more supply chain attacks in 2021 than in 2020. With half of the attacks being attributed to Advanced Persistence Threat actors" - "Threat Landscape for Supply Chain Attacks" 2021, https://www.enisa.europa.eu<br/>
  Do your best to protect you and your customer.

tags:
 - HSM
 - Security
 - Supply chain
 - PGP
 - GPG
---

# PGP keys best-practices for developers

Supply-chain attacks are the Y2K of 2020.

    "It is estimated that there will be four times more supply chain attacks in 2021 than in 2020. With half of the attacks being attributed to Advanced Persistence Threat actors"
    - "Threat Landscape for Supply Chain Attacks" 2021, https://www.enisa.europa.eu

The most challenging part regarding PGP is to understand how the subkeys need to be structured. If you get that right, you can churn away with peace of mind.

## Rationale

In the ever-evolving cyber threat landscape supply-train attacks have been utilized with high efficacy.
The most notorious of which is the SolarWinds-incident.
There have been multiple attacks and attempts on the PHP Core, and numerous others.
It is especially stupefying, when the tainted release becomes automatically built and signed by the build process, as safe to use.

Traditionally git only checks for access control to the repositories, and a few permissions to write/read/force changes to the git history.
There is no mechanism to prevent spoofing the author, sign-offers, or even the committer of the changes.

Using signed git commits and tags is a good way of doing your part to enforce Authenticity, Integrity and Non-repudiability, of the software source code.

## Sponsored by

Technology and Innovation Institute of the United Arab Emirates, Secure Systems Research Center

## PGP best-practices

A big part of using PGP-keys is understanding the complete key-lifecycle, from creating them, to using them safely, to revoking stolen keys or recovering lost passwords and broken hardware security modules.
Another aspect of complexity is introduced from our mobile work lifestyle, where encrypted information needs to be accessible from mobile phones, tablets, laptops and servers, and preserving your core digital identity even after your phone gets stolen.
Poorly implemented key-management strategies will work initially, but cannot survive the inevitable changes that face maintaining a long-term digital identity in this quantum age.

### PGP key capabilities

PGP keys have the following capabilities:

- (C) Certify, aka sign other keys. Within the PGP-key: create new User Identities, new Subkeys, change trust of an identity and priority of identities.
- (S) Sign documents/files/anything. This means that you sign the message with your personal secret signing key and thus the message is cryptographically proven to be "non-repudiately" signed by you.
- (E) Encrypt documents/messages/anything. This is how you make the message "confidential", aka. only readable by the intended recipient or recipients. PGP actually works via "envelope-encryption", where the message is actually encrypted with a symmetric cipher, and the symmetric cipher passphrase is asymmetrically encrypted using each recipients public encryption key. This way the big message need not be encrypted multiple times for each recipient, but all the recipients can share the one minimal secret.
- (A) Authentication is used to authenticate to services, such as OpenSSH connections using a gpg-agent.

### The importance of (C)

It must be understood, that protecting the private master key (the one with (C)ertify-capability) is the cornerstone of maintaining your digital identity. If you lose it you lose yourself. Thus it is often recommended to not carry the private master-key with you (well maybe in a HSM). Simply use Subkeys for all daily operations.
Traditionally you build a web-of-trust for your public master key, and all subkeys, current and future, can enjoy the same web-of-trust built on the public master key.
If PGP is used only for work, this is not such a big issue, as the web-of-trust can be rebuilt. However if you base your global private digital identity on your master key and the web-of-trust you have built with like-minded people, recovering from that loss might be impossible.

All the key recovery scenarios revolve around using the master key to revoke the stolen/lost/obsolete subkeys you use in daily operations.

### Separate the (S) from the (E)

Basically cryptographical keys can be used to encrypt and decrypt messages. There is no real algorithmical distinction between signing and encrypting. Signing is a process of encrypting a condensed hash or a message, intended to be decrypted by the recipients. This way the content can be public, with digitally verified signatures.
One attack vector is to trick gpg or a hardware security module to mix signing and encrypting, thus breaking the encryption on a message by feeding it to the encryptor as a message hash that needs signing. So if you were to use the same key for (S) and (E), this attack might be possible.

### Separate the (S) from the (C)

By default the GPG key generation creates a master-key which can (C)ertify and (S)ign. This is the default for Nitrokey Pro device initialization too. This enables the key-holder to easily (C)ertify other persons' PGP-Identities, without having to recover the PGP master key from the secure storage (eg. hidden encrypted in a forest). It is very convenient to some extent.

Now comes the real trick.
Let us presume that your keys are safely tucked in a Nitrokey Pro 2 security module, and you can sign and verify git commits, authenticate to ssh-connections, sign and encrypt email. How about reading your email from your mobile phone? To enable this, you need to copy your (S)igning and (E)ncryption keys to your phone, and use them for example with OpenKeyChain. If the (C) and (S) are bundled together, you cannot later separate them. You don't want your private master key on a mobile phone, well maybe with the degoogled high security GrapheneOS with TitanM-chip as the onboard HSM.

### Cipher recommendation

The current cipher recommendation from https://www.enisa.europa.eu is rsa3072 (10-20 years of confidentiality). Using rsa4096 is much slower and "only" 65 000 times more difficult to break (20-50 years of confidentiality). The incoming quantum encryption techniques might make short work (5 years) of rsa encryption, but that remains to be seen.
The performance drop from rsa2048 to rsa4096 is so significant, that the big cloud hosting providers simply cannot do it.
Some HSMs, like the Nitrokey Pro 2, cannot compute rsa4096 in a reasonably quick manner, as it might take more than 6s for cryptographic operations.
'gpg'-tool automatically updates the recommendation, so if it is different, use that instead.
If you are using rsa2048, consider migrating to rsa3072.

### Expiration recommendation

The PGP key must expire.
Make a calendar date for yourself to extend the key validity, or you will forget.
This is to enable the key to be automatically cleaned from the keyservers, if you happen to lose access to the master key or the stored revocation tokens. It also increases the general validity of your key in the eyes of other humans and machines as well.
It might feel inconvenient, but it is surprisingly easy to extend the key validity. While doing that, it is a good time to rehearse a bit of gpg and check you still have access to the backup media.

### Passwords

During the creation and operation of PGP-keys, you need 3 separate passwords.

- HSM PIN and PGP-key passphrase can be the same. This is because when you use the PGP-key from your mobile phone, you need to "unlock" it with a passphrase, and when you use the HSM from your laptop, you need the HSM PIN for exactly the same operations.
- HSM Admin PIN and PGP-key backup encryption passphrase.
- HSM Reset PIN, alternatively the PGP-key backup encryption passphrase could be the same.

Depending on your preferences, you might want to use an alternative set of passwords.

It is recommended to save the all the PIN-codes and passphrases on a piece of paper and hide it in a secure location. This is because you will most certainly forget one or all of the passphrases.

## Howto - PGP-key creation

### Hardware recommendations

This howto is written with the focus of using a USB HSM to authenticate the user to high-security services. The howto can be followed without possessing all of the hardware recommendations.

- A separate USB HSM to protect the keys. Nitrokey 2 Pro in this case.
- A separate USB memory drive, to store the encrypted master key.
- A separate "airgapped" linux PC for key creation. The level of paranoia needed is left to the reader. I used a fresh installation of RaspbianOS on Raspberry Pi4 as I had them lying around a plenty.
- A secure mobile phone to read your email. GrapheneOS is an excellent choice, since it offers secure boot and the whole OS is signed from the boot upwards. If somebody steals your phone, there is no way they can access the contents, or tamper with the OS. It also offers some protection against Western nation states as it is degoogled.

### Preparing the PGP-keys

This should be done in the "airgapped" dedicated key-creation PC, but follow your current means and level of motivation. Your work-laptop is probably reasonably safe, unless it is running an unsafe operation system.

There are many good tutorials online about this very process, so if in doubt about exact commands or usage, take a look at those.
Especially (https://www.kernel.org/doc/html/v5.8/process/maintainer-pgp-guide.html)[the linux kernel maintaners guide].
However the instructions here enable the aforementioned features of federated identity access which seems to be missing from the other instructables.

gpg v2.* is required.

prepare your own playspace for key creation. This way you can possibly create multiple keys, or help others create theirs in the same airgapped device, without potentially exposing each others to your keys, or breaking anything unintentionally.

    $ mkdir -p ~/keys/solita
    $ cd ~/keys/solita

### Begin the key creation

    $ gpg --homedir=.gnupg --full-generate-key --expert

    Your selection? *(8) RSA (set your own capabilities)*

Toggle capabilities until you have only *Certify* left.

    Press Q to finish.

    What keysize do you want? (3072) *3072*

    Please specify how long the key should be valid.

    Key is valid for? (0) *1y*

Take note that the date is actually correct. An airgapped PC might be living in a completely arbitrary date.

    Real name: Olli-Antti Kivilahti
    Email address olli-antti.kivilahti@solita.fi
    Comment:

You must create a passphrase to protect the master key.

```
gpg: key 585D57073491F244 marked as ultimately trusted
gpg: revocation certificate stored as '/home/pi/keys/solita/.gnupg/openpgp-revocs.d/F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E.rev'
public and secret key created and signed.

pub   rsa3072 2021-09-15 [C] [expires: 2022-09-15]
      F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E
uid                      Olli-Antti Kivilahti <olli-antti.kivilahti@solita.fi>
```

Congratulations. You are now the owner of a digital identity certificate.

Take note of the PGP-key fingerprint, in this case 'F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E'.
Also copy the revocation certificate for easy access.

    $ cp /home/pi/keys/solita/.gnupg/openpgp-revocs.d/F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E.rev olli-antti.kivilahti@solita.fi.rev

We will later bundle it with the unencrypted portion of the PGP-key backup.

### Create the subkeys

Now we create three subkeys, one for each capability.

    $ gpg --homedir=.gnupg --edit-key --expert olli-antti.kivilahti@solita.fi
    $ addkey

    Your selection? *(8) RSA (set your own capabilities)*

Now repeat the addkey command, until you have three separate subkeys with distinct capabilities, (S) (E) (A).
Finally save the changes.

    $ save

you should have the following key, user identity and subkeys.

    $ gpg --homedir=.gnupg --list-keys

```
pub   rsa3072 2021-09-15 [C] [expires: 2022-09-15]
      F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E
uid           [ultimate] Olli-Antti Kivilahti <olli-antti.kivilahti@solita.fi>
sub   rsa3072 2021-09-15 [S] [expires: 2022-09-15]
sub   rsa3072 2021-09-15 [E] [expires: 2022-09-15]
sub   rsa3072 2021-09-15 [A] [expires: 2022-09-15]
```

### Backup the keys

Now export the keys. This might not be strictly necessary, but if the format of gpg2 local storage changes some years into the future, it is easier to import the exported keys.

    $ gpg --homedir=.gnupg --export --armor olli-antti.kivilahti@solita.fi > olli-antti.kivilahti@solita.fi.pub
    $ gpg --homedir=.gnupg --export-secret-keys --armor olli-antti.kivilahti@solita.fi > olli-antti.kivilahti@solita.fi.key

Then plug in the USB drive, have it mounted and ready to be written into. Make sure that at no point any part of unencrypted private key material enters the USB drive. If this happens, you must deep-format the USB drive to make the private key unrecoverable in it's clear-text form. Simply "shred <filename>" might not help, due to the internal mechanics of persistent storage implementations.
If you follow these instructions, that shouldn't happen.

    $ tar -czf - .gnupg olli-antti.kivilahti@solita.fi.* | gpg -c - > /media/pi/key/olli-antti.kivilahti@solita.fi.tar.gz.gpg
    $ cp olli-antti.kivilahti@solita.fi.pub /media/pi/key/
    $ cp olli-antti.kivilahti@solita.fi.rev /media/pi/key/

Now test that the backup worked.

    $ mkdir ../testing
    $ cd ../testing
    $ gpg -d /media/pi/key/olli-antti.kivilahti@solita.fi.tar.gz.gpg | tar -xzf -
    $ ls -lah

The output should look like this.

```
total 32K
drwxr-xr-x 3 pi pi 4.0K Sep 15 16:24 .
drwxr-xr-x 6 pi pi 4.0K Sep 15 16:24 ..
drwx------ 5 pi pi 4.0K Sep 15 16:08 .gnupg
-rw-r--r-- 1 pi pi  11K Sep 15 16:12 olli-antti.kivilahti@solita.fi.key
-rw-r--r-- 1 pi pi 5.3K Sep 15 16:12 olli-antti.kivilahti@solita.fi.pub
-rw------- 1 pi pi 1.7K Sep 15 16:10 olli-antti.kivilahti@solita.fi.rev
```

The contents of your backup USB disk should look like this.

    $ ls -lah

```
-rw-r--r--  1 pi   pi   5.3K Sep 15 16:23 olli-antti.kivilahti@solita.fi.pub
-rw-------  1 pi   pi   1.7K Sep 15 16:23 olli-antti.kivilahti@solita.fi.rev
-rw-r--r--  1 pi   pi   112K Sep 15 16:26 olli-antti.kivilahti@solita.fi.tar.gz.gpg
```

The .key-file is only within the backup archive.

Finally get back to your working directory.

    $ cd ../solita

Congratulations. Now you have double encrypted your private master key and have a reliable backup.
It is smart to copy the backup contents to yet another USB-drive. This is something you can have accessible if you need to (C)ertify other people's User Identities attached to the respective public master keys to build your web-of-trust.
The other backup can be archived into a bank-vault together with the 3 passphrases you need.

### Prepare your HSM (OPTIONAL)

scdaemon needs to be installed.

    $ sudo apt install scdaemon
    $ gpg-agent restart

Plug in your HSM. Check if the kernel detects the device.

    $ dmesg | less

If your HSM was detected, check if gpg understands it.

    $ gpg --homedir=.gnupg --card-status

You should see something like this.

```
Reader ...........: 20A0:4108:0000D23DA0A44DEEF800ADAA:0
Application ID ...: D27600012401030DA0A44DEEF82E0000
Version ..........: 3.4
Manufacturer .....: ZeitControl
Serial number ....: 0000ADAA
Name of cardholder: [not set]
Language prefs ...: de
Sex ..............: unspecified
URL of public key : [not set]
Login data .......: [not set]
Signature PIN ....: forced
Key attributes ...: rsa2048 rsa2048 rsa2048
Max. PIN lengths .: 64 64 64
PIN retry counter : 3 0 3
Signature counter : 0
KDF setting ......: on
Signature key ....: [none]
Encryption key....: [none]
Authentication key: [none]
General key info..: [none]
```

Now the HSM has been successfully detected and is ready to be configured and used.

Next you need to change the PIN-codes.

    $ gpg --homedir=.gnupg --card-edit
    $ admin
    $ passwd

Set all the PIN-codes, PIN, Admin PIN and Reset Code.
It is up to you how much personal information you want to include in your HSM. This might be used against you to for example prove that the HSM belongs to you and force you to confess the PIN-codes.
It is beneficial to set the 'url'-value of the HSM later to point to the fingerprint of your master key, when you have published your key to a public keyserver or website.

Next we need to copy the keys into the HSM. The copy-operation replaces the local private subkeys with stubs. On the outside they look like private subkeys, but they are not.
This process moves only the subkeys into the HSM, the private master key remains in the local keychain.
Make a local copy of the .gnupg-dir

    $ cp -r .gnupg .gnupg2

The HSM needs to be plugged out and put back in again to be usable from the new homedir. Do that now.

Copy all the *subkeys* into the HSM.
When asked:

    Please select where to store the key:

Make sure to match the subkey capabilities to the HSM key slots.
The subkey with capability (S) is the (1) Signature key
Capability (E) is the (2) Encryption key
Capability (A) is the (3) Authentication key

    $ gpg --homedir=.gnupg2 --edit-key F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E
    $ key 1
    $ keytocard
    $ key 1
    $ key 2
    $ keytocard
    $ key 2
    $ key 3
    $ keytocard
    $ save
    $ rm -r .gnupg2

Congratulations. Now the HSM is ready to be used.

### (S)igning and (E)ncryption keys for the mobile devices (OPTIONAL)

To move only the minimum amount of private key material to the mobile phone, we need to do key-stripping.
PGP-keys can function even without the presence of the private master-key, and this is an advanced security feature of PGP.
The preservation of identity is based around this functionality. Everybody can see from the subkey itself, that the subkey is a descendant of the private master key. Everybody can see the signatures (web-of-trust) on the public master key. Thus the verification power of the master-key is usable by all the subkeys, even not-yet-existing ones. Revocation of subkeys doesn't diminish the trust on the master key.
So subkeys are in-a-way reusable. It is good to understand, that if a subkey is lost, all the material encrypted with the key cannot be decrypted anymore. Thus we only revoke the subkey, instead of deleting it. Your keychain (but not HSM) can contain any amount of revoked subkeys, and they can be used to decrypt old messages. However revoked keys can no longer be used to encrypt anything. The master-key cannot decrypt messages encrypted with descendant subkeys.

The idea here is to strip the private master key and the private (A)uthentication subkey, as those are not needed on the mobile device.
Then the remaining keys are encrypted and moved to the mobile device.

Make a copy of the original PGP master key.

    $ cp -r .gnupg .gnupg3

Check the subkey signatures.

    $ gpg --homedir=.gnupg3 --edit-key F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E

```
Secret key is available.

sec  rsa3072/D23DA0A44DEEF244
     created: 2021-09-15  expires: 2022-09-15  usage: C   
     trust: ultimate      validity: ultimate
ssb  rsa3072/D23DA0A44DEE3B7E
     created: 2021-09-15  expires: 2022-09-15  usage: S   
     card-no: 0005 ADAAADAA
ssb  rsa3072/D23DA0A44DEE53EC
     created: 2021-09-15  expires: 2022-09-15  usage: E   
     card-no: 0005 ADAAADAA
ssb  rsa3072/D23DA0A44DEEF82E
     created: 2021-09-15  expires: 2022-09-15  usage: A   
     card-no: 0005 ADAAADAA
[ultimate] (1). Olli-Antti Kivilahti <olli-antti.kivilahti@solita.fi>
```

Strip away.

    $ gpg --homedir=.gnupg3 --delete-secret-key F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E

    Delete this key from the keyring? (y/N) *y*

Now be careful, gpg starts asking you questions about do you want to delete this key/subkey.
Only delete the private master *key*. When gpg prompts to delete *subkey*, press "No".

Next delete the (A)uthentication private subkey. Notice the exclamation mark at the end!

    $ gpg --homedir=.gnupg3 --delete-secret-key D23DA0A44DEEF82E!

You can verify that you have successfully stripped the excess private keys, from the #-character after the sec and ssb -tags.

    $ gpg --homedir=.gnupg3 --list-secret-keys F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E

```
sec#  rsa3072 2021-09-15 [C] [expires: 2022-09-15]
      F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E
uid           [ultimate] Olli-Antti Kivilahti <olli-antti.kivilahti@solita.fi>
ssb   rsa3072 2021-09-15 [S] [expires: 2022-09-15]
ssb   rsa3072 2021-09-15 [E] [expires: 2022-09-15]
ssb#  rsa3072 2021-09-15 [A] [expires: 2022-09-15]
```

Now export and encrypt the keys for transit.

    $ gpg --homedir=.gnupg3 --export-secret-keys F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E > tomobile.key
    $ gpg -c tomobile.key

Move the file tomobile.key.gpg to your mobile phone.

Android apps OpenKeyChain and K-9 Mail work really well together. It is very easy to configure them, and in no time you will be (S)igning and (E)ncrypting email and other documents.

Finally clean the temporary homedir.

    $ rm -r .gnupg3

### Publish your digital PGP-identity

An important part of PGP is making your digital identity known and available to people. When you sign a git commit and it is pushed to the central repository, you need to tell the central repository what your public keys is, or where it can be found. Otherwise the server cannot verify your identity.
When a co-developer pulls code you have signed, he needs to get access to your public key, to verify your identity.
When you plug your HSM to another laptop, you need to make the public key available for the local gpg-keychain, or the local encryption requests cannot be connected to the HSM.
When somebody receives email you have signed, they need your public key to decrypt and verify.
An important part of this identity verification is the web-of-trust.
If your recipient knows somebody or somebodies, who also know you, and can vouch for your public key strongly enough, the recipient can implicitly trust in their verification of your digital identity. This way the recipient doesn't need to do strong verification of the version of your public key the recipient received, against the version you have on your machine.
There is ample documentation online about the web-of-trust, so no deeper dive is needed here.

To get started, you should publish your public key to one of the public keyservers. It takes some hours for the key to propagate and be searchable from the public PGP-key infrastructure.
Also you need to manually publish changes to your keys when those are changed. For example if you revoke one of the subkeys, or extend the validity of the certificate.

    $ gpg --homedir=.gnupg --keyserver keys.openpgp.org --send-key F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E

keys.openpgp.org is a good cluster of keyservers, and they send you an email upon key-submission asking you to confirm whether or not you want your key to be searchable by your email address, or just with the fingerprint. Thank GDPR.

You can also share the public key automatically in all your signed emails.

You should configure a cronjob to periodically synchronize the local keystore with changes in the public keyservers, so you can receive automatic revocation notifications and expiration extensions. Change the numbers 23 and 22 to something else, so not everybody who follows this howto spams the keyservers at the same time.

    $ echo "23  22  * * *   pi      /usr/bin/gpg --refresh-keys" > /etc/cron.d/gpg

#### Link HSM to keyserver

To make it easy to use your HSM on different machines, it is recommended to share your public key online.
To configure the HSM to fetch the public key from a predefined URL, set the 'url'-attribute of the HSM to the fingerprint, eg.

    $ gpg --homedir=.gnupg --card-edit
    $ admin
    $ url
    URL to retrieve public key: *https://keys.openpgp.org/vks/v1/by-fingerprint/F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E*
    $ quit

When you plug your HSM to another machine, to access the HSM capabilities, you need to fetch the public key.

    $ gpg --card-edit
    $ fetch
    $ quit

### Move the keys to the development machine

The last step is to make the subkeys available for your daily use.

#### If you created the keys on your work laptop

just make sure the new keys are in your local system default keychain, at ~/.gnupg
You can make sure with these commands.

    $ gpg --import ~/keys/solita/*.key

#### If you used an "airgapped" machine without a HSM

You need to recover the backup and import the private master key.

    $ cd ~
    $ gpg -d /media/kivilahtio/keys/olli-antti.kivilahti@solita.fi.tar.gz.gpg | tar -xzf -
    $ gpg --import olli-antti.kivilahti@solita.fi.key
    $ rm olli-antti.kivilahti@solita.fi.*

#### If you used an "airgapped" machine with a HSM

Follow instructions in #Prepare your HSM (OPTIONAL)

If you shared your key to a public website/service, follow instructions here #Link HSM to keyserver

Otherwise you need to import the public key from your backup USB drive.

    $ gpg --import /media/kivilahtio/olli-antti.kivilahti@solita.fi.pub

Without the public master key of the subkeys inside the HSM, encryption requests cannot be directed to the HSM.

## Howto - Development workflows

So now that we have PGP-keys set, we can focus on how to use them.

### Signed git commits

To benefit from the security of signed git commits, the repository must not accept unsigned commits.
Here are instruction on how to enforce signed commits in your repos.
[GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches#require-signed-commits)
[GitLab](https://docs.gitlab.com/ee/push_rules/push_rules.html#caveat-to-reject-unsigned-commits-push-rule)
[BitBucket](https://confluence.atlassian.com/bitbucketserver/using-gpg-keys-913477014.html#UsingGPGkeys-add)

If you are not a big fan of massive and cumbersome graphical Git servers, you can implement a very lightweight solution using a simple git-server accessible via ssh.
[git server](https://www.linux.com/training-tutorials/how-run-your-own-git-server/)
[git-hooks](https://githooks.com/)
[git verify-commit](https://git-scm.com/docs/git-verify-commit)

Here is a short summary of what needs to be done to start using signed git commits.

    $ git config --global user.signingkey F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E
    $ git config --global commit.gpgsign true
    $ git config --global log.showSignature true
    $ git config --global tag.gpgsign true

After you have signed and committed changes to the central repository, you should never ever delete your keys. When you revoke old keys, for example to migrate to a stronger cipher (or in case of a theft), you, your colleagues and the git server still need to have access to your old revoked key, in order to verify the existing commits in version control.

#### Distributing PGP-keys between colleagues

There are existing processes documented online, many involve setting up some kind of a private keyserver or a mailing list.

##### Existing public PKI

Easiest is to rely on the existing PKI, such as keys.openpgp.org
Sometimes due to the security-requirements of the project, it might not be desirable, especially if the PGP-key identities (firstname.surname@client.com) cannot be public. The public PKI doesn't work without publishing the User ID (firstname.surname@client.com) for all to search.

Receiving the public key of a colleague this way is easy.

    $ gpg --keyserver keys.openpgp.org --search-keys olli-antti.kivilahti@solita.fi

##### Internal wiki    

One could simply create a project wiki, where everybody shares their own public PGP master key. This leverages existing infrastructure and is very easy to get started with.

    $ gpg --export --armor F9443F50BED23DA0A44DEEAAD0CB86C4E2684F3E > olli-antti.kivilahti@solita.fi.pub

Upload and download public keys to your wiki. Then import the new public keys.

    $ gpg --import esko.oramaa@solita.fi.pub

This way everybody can also locally verify the git/email/etc signatures.

When uploading the public key to the wiki, remember to upload the public key to your git server too.

### GPG Agent Forwarding

When developing features in remote servers and dev-containers, you have the same signing and verification needs as locally. It would be impractical to virtually mount your HSM to every server you work with.
You MUST ABSOLUTELY NOT copy your private keys to any remote container or server, especially with multiple users. Not even ssh-keys.
GPG Agent Forwarding allows you to use your encryption capabilities in remote environments over the ubiquituous ssh.

There are several good tutorials online on how to configure your environments, such as

- [GPG Agent Forwarding](https://wiki.gnupg.org/AgentForwarding)

Be aware that the GPG Agent socket that is forwarded to the remote machine, exposes a limited set of capabilities.
So normal commands such as

    $ gpg --card-status

```
gpg: error getting version from 'scdaemon': Forbidden
gpg: selecting card failed: Forbidden
gpg: OpenPGP card not available: Forbidden
```

    $ gpg -c file.txt

```
gpg: problem with the agent: Forbidden
gpg: error creating passphrase: Operation cancelled
gpg: symmetric encryption of 'test' failed: Operation cancelled
```

Do not work by default.

However you can sign and verify git commits.

    $ git commit -S

And if the forwarding works, you should receive your normal desktop popup PIN-entry notification.

### ssh authentication using a HSM/PGP-key

There are many good tutorials on the topic, such as:

- https://opensource.com/article/19/4/gpg-subkeys-ssh

A short summary is condensed here.

    $ echo "enable-ssh-support" > ~/.gnupg/gpg-agent.conf
    $ echo '
    export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket)
    gpgconf --launch gpg-agent
    ' > ~/.bashrc

Get the keygrip of your (A)uthentication subkey.

    $ gpg --list-keys --with-keygrip

And paste it here.

    $ echo 7710BA0643CC022B92544181FF2EAC2A290CDC0E >> ~/.gnupg/sshcontrol

Finally reload your shell to update the changes. Then get the ssh-version of your (A)uthentication subkey.

    $ ssh-add -L

And put that into the /home/username/.ssh/authorized_keys of the servers you want to login to.

#### SSH ProxyCommand over SSH ForwardAgent

When jumping the ssh-connection over multiple hosts, it is important to not confuse these two terms.

ForwardAgent aka Agent forwarding, creates a local UNIX socket on the remote host. This socket can be easily abused by a rooted attacker to use your ssh-agent to access all other servers with your credentials.
You can protect against this by hardening the ssh-agent with

    $ ssh-add -c -t 30m

ProxyCommand simply forwards the connection immediately to the next host, without creating a local agent forwarding socket for each host jumped.

GPG Agent Forwarding has a similar vulnerability. However gpg by default always asks the user for confirmation to use the cryptographic capabilities from the local developer machine.
Thus the gpg-agent is by default hardened against unauthorized use.

See [the Mozilla Foundation's excellent article on he matter](https://infosec.mozilla.org/guidelines/openssh.html).

# Thank you for reading

I hope this article helped you have a more in-depth understanding of PGP and GPG.

Below you find sources used to write this article in no particular order.
Especially the Linux Kernel Developers guide is a good read.



https://www.kernel.org/doc/html/latest/process/maintainer-pgp-guide.html
https://people.eecs.berkeley.edu/~tygar/papers/Why_Johnny_Cant_Encrypt/OReilly.pdf
https://docs.gitlab.com/ee/user/project/repository/gpg_signed_commits/
https://docs.github.com/en/github/authenticating-to-github/managing-commit-signature-verification/signing-commits
https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work
https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches#require-signed-commits
https://docs.gitlab.com/ee/push_rules/push_rules.html#caveat-to-reject-unsigned-commits-push-rule
https://www.linux.com/training-tutorials/how-run-your-own-git-server/
https://githooks.com/
https://git-scm.com/docs/git-verify-commit
https://wiki.gnupg.org/AgentForwarding
https://www.venafi.com/blog/solarwinds-sunburst-attack-explained-what-really-happened
https://www.bleepingcomputer.com/news/security/phps-git-server-hacked-to-add-backdoors-to-php-source-code/
https://riseup.net/en/security/message-security/openpgp/best-practices
https://www.enisa.europa.eu/about-enisa/structure-organization/national-liaison-office/news-from-the-member-states/estonia-cryptographic-algorithms-lifecycle-report-2016-published
