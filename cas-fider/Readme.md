# cas-fider

```bash
helm dep up postgresql
helm dep up fider
helm dep up cas-fider

# install in dev
helm -n "wksv3k-dev" install --set fider.host.prefix="ciip-portal-wksv3k-dev-feedback" cas-fider cas-fider

# install in test
helm -n "wksv3k-test" install --set fider.host.prefix="ciip-portal-wksv3k-test-feedback" cas-fider cas-fider

# install in prod
helm -n "wksv3k-prod" install cas-fider cas-fider
```
