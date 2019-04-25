/^schema: deckhand/i apiVersion: deckhand.airshipit.org/v1alpha
1,$s;schema: deckhand/;kind: Deckhand;g
/^schema: armada/i apiVersion: armada.airshipit.org/v1alpha
1,$s;schema: armada/;kind: Armada;g
/^schema: promenade/i apiVersion: promenade.airshipit.org/v1alpha
1,$s;schema: promenade/;kind: Promenade;g
1,$s;^sdata:;spec:;g
1,$s;/v1$;;g
/schema: metadata/d
/storagePolicy/d
