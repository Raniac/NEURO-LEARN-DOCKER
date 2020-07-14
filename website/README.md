# NEURO-LEARN-WEBSITE

## Start ```neuro-learn-website:dev``` Container

```bash
frontend$ npm run build
website$ sudo killall -9 nginx
website$ cd .. && docker run -it --rm --network host neuro-learn-website:dev
```
