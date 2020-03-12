## Fider Image build (customized)

We reuse the customized fider image and build steps from the MDS team (https://github.com/bcgov/mds/)

Since BC Gov's SMTP configuration does not support smtps, and Fider's SMTP Go library enforces smtps, we fork the code so that we remove the authn/authz from our deployment.

To create an image off this forked code:

```bash
oc -n wksv3k-tools new-build --strategy=docker --to='fider-notls:latest' https://github.com/garywong-bc/nrm-fider#v0.18.0.notls
```

To tag this image to match `major.minor` version of Fider:

```bash
oc -n wksv3k-tools tag fider:latest fider:0.18.0
```
