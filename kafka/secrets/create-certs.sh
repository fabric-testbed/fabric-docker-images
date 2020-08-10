#!/bin/bash

set -o nounset \
    -o errexit \
    -o verbose \
    -o xtrace

# Generate CA key
openssl req -new -x509 -keyout snakeoil-ca-1.key -out snakeoil-ca-1.crt -days 365 -subj '/CN=ca1.test.fabric-testbed.net/OU=TEST/O=FABRIC/L=Lexington/S=Ky/C=US' -passin pass:fbtestkfk -passout pass:fbtestkfk
# openssl req -new -x509 -keyout snakeoil-ca-2.key -out snakeoil-ca-2.crt -days 365 -subj '/CN=ca2.test.confluent.io/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US' -passin pass:confluent -passout pass:confluent

# Kafkacat
openssl genrsa -des3 -passout "pass:fbtestkfk" -out kafkacat.client.key 1024
openssl req -passin "pass:fbtestkfk" -passout "pass:fbtestkfk" -key kafkacat.client.key -new -out kafkacat.client.req -subj '/CN=kafkacat.fabric-testbed.net/OU=TEST/O=FABIRC/L=Lexington/S=Ky/C=US'
openssl x509 -req -CA snakeoil-ca-1.crt -CAkey snakeoil-ca-1.key -in kafkacat.client.req -out kafkacat-ca1-signed.pem -days 9999 -CAcreateserial -passin "pass:fbtestkfk"



for i in broker1 broker2 broker3 producer consumer
do
	echo $i
	# Create keystores
	keytool -genkey -noprompt \
				 -alias $i \
				 -dname "CN=$i.fabric-testbed.net, OU=TEST, O=FABRIC, L=Lexington, S=Ky, C=US" \
				 -keystore kafka.$i.keystore.jks \
				 -keyalg RSA \
				 -storetype pkcs12 \
				 -storepass fbtestkfk \
				 -keypass fbtestkfk

	# Create CSR, sign the key and import back into keystore
	keytool -keystore kafka.$i.keystore.jks -alias $i -certreq -file $i.csr -storepass fbtestkfk -keypass fbtestkfk

	openssl x509 -req -CA snakeoil-ca-1.crt -CAkey snakeoil-ca-1.key -in $i.csr -out $i-ca1-signed.crt -days 9999 -CAcreateserial -passin pass:fbtestkfk

	keytool -keystore kafka.$i.keystore.jks -alias CARoot -import -file snakeoil-ca-1.crt -storepass fbtestkfk -keypass fbtestkfk

	keytool -keystore kafka.$i.keystore.jks -alias $i -import -file $i-ca1-signed.crt -storepass fbtestkfk -keypass fbtestkfk

	# Create truststore and import the CA cert.
	keytool -keystore kafka.$i.truststore.jks -alias CARoot -import -file snakeoil-ca-1.crt -storepass fbtestkfk -keypass fbtestkfk

  echo "fbtestkfk" > ${i}_sslkey_creds
  echo "fbtestkfk" > ${i}_keystore_creds
  echo "fbtestkfk" > ${i}_truststore_creds
done
