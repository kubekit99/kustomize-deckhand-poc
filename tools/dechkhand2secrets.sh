#!/bin/bash
sed -i '/^kind: DeckhandCertificate$/a type: Opaque' airship.yaml
sed -i '/^kind: DeckhandCertificateAuthority$/a type: Opaque' airship.yaml
sed -i '/^kind: DeckhandCertificateAuthorityKey$/a type: Opaque' airship.yaml
sed -i '/^kind: DeckhandCertificateKey$/a type: Opaque' airship.yaml
sed -i '/^kind: DeckhandPassphrase$/a type: Opaque' airship.yaml
sed -i '/^kind: DeckhandPrivateKey$/a type: Opaque' airship.yaml
sed -i '/^kind: DeckhandPublicKey$/a type: Opaque' airship.yaml
