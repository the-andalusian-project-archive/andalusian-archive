# Image manifest

Lane P3, 2026-09-27. One row per image file published under `assets/images/`.
Every row records the file as it now exists in this repository, with the
sha256 of its bytes, and the source URL and capture timestamp lane F1
recorded for it. The staged originals this table was built from lived under
`_staging/`, which is deleted at the end of the recovery; `assets/images/`
is the surviving copy.

## Totals

| | |
|---|---|
| Staged files received | 335 (294 `.jpg`, 40 `.png`, 1 `.pdf`), 70,818,428 bytes |
| Byte-identical duplicate groups | 47 (covering 96 files) |
| Files removed by deduplication | 49, reclaiming 6,534,920 bytes (6.23 MB) |
| Unique files after deduplication | 286, 64,283,508 bytes (61.31 MB) |
| Held back from `assets/images/` | 2 (1 PDF by instruction, 1 HTML page served with an image name) |
| **Published image files** | **284, 61,613,790 bytes (58.76 MB)** |
| Referenced by a published work page | 21 (all rewired to a local path) |
| Catalogued but not embedded in any page | 263 |
| Alt text written from viewing the image | 37 |
| Alt text written honestly generic | 247 |
| Images withheld on privacy grounds | 0 |

### Licensing posture

These images were published alongside the author's own writing on the
author's own sites (`asadullahali.wordpress.com` and the domain it served).
They are archived here **for preservation, with attribution to Asadullah Ali
al-Andalusi**, as part of the record of the work. This archive asserts no
new licence over them and does not relicense third-party material it
happens to hold: a reader who wants to reuse an image should satisfy
themselves about its provenance from the `Source URL` column, which points
at the host the author published it from. Several images are the author's
own polemical material depicting third parties, including named living
people; they are preserved unaltered because the archive's job is to
preserve the work, not to referee it.

## Published images

`sha256` is of the published bytes. `Capture` is the lane F1 retrieval
timestamp from `_staging/mirror/manifest.json`. `Work` gives the work slug
the image was published with; `Page` says whether the image is inline on
that work's page or catalogued only.

### `001_1.png`

| | |
|---|---|
| sha256 | `62ebe249b52b9df89f65d1c727ffcb8d078a34a40306df50310a6c6bcdbe559d` |
| Bytes | 17,677 |
| Dimensions | 750x335 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/05/1.png |
| Capture | 2026-09-27T14:18:52+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src` |
| Work | `my-views-on-the-punishment-for-apostasy` (My Views On the Punishment For Apostasy), `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah), `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'My Views On the Punishment For Apostasy' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `002_4ad90-desert-man.jpg`

| | |
|---|---|
| sha256 | `e09fa93774d4b4b277978d0ca8beb9eefee1342be001ba34851706df98dc9983` |
| Bytes | 25,605 |
| Dimensions | 852x480 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4ad90-desert-man.jpg |
| Capture | 2026-09-27T14:18:54+05:30 |
| Role in the post | `featured_media` |
| Work | `my-views-on-the-punishment-for-apostasy` (My Views On the Punishment For Apostasy) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A man seen from behind in a white shirt and dark trousers, standing with his arms slightly outstretched on bare sand dunes under a clear sky. |
| Alt text basis | written after viewing the image |

### `003_f4206-saajidapostasy.jpg`

| | |
|---|---|
| sha256 | `82d7177910f05ff4f03b34ff50e3b8fd123b117685e47fa763ef30df70105212` |
| Bytes | 86,091 |
| Dimensions | 661x618 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/f4206-saajidapostasy.jpg |
| Capture | 2026-09-27T14:18:55+05:30 |
| Role in the post | `img:src` |
| Work | `my-views-on-the-punishment-for-apostasy` (My Views On the Punishment For Apostasy) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'My Views On the Punishment For Apostasy' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `004_01f91-danielhaya14.jpg`

| | |
|---|---|
| sha256 | `a87a15cc0c6c7b1a2f8d18964342e8a7f7eee5b46b3dfce2657203e77d318439` |
| Bytes | 163,814 |
| Dimensions | 1361x889 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/01f91-danielhaya14.jpg |
| Capture | 2026-09-27T14:18:57+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | YouTube thumbnail of a Muslim Skeptic video: a man in a red shirt beside a panel photograph captioned 'Linda Sarsour and Bob Bland'. |
| Alt text basis | written after viewing the image |

### `005_03a67-specialthanks-1.jpg`

| | |
|---|---|
| sha256 | `3349800f1a342f00ad89c2aeb01b09a15d4d76880258686b7346203414310f73` |
| Bytes | 253,281 |
| Dimensions | 991x686 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/03a67-specialthanks-1.jpg |
| Capture | 2026-09-27T14:18:58+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `006_04292-hijab3-1.jpg`

| | |
|---|---|
| sha256 | `9389a538d4dec383ecc5efa48d87d6dbb28c583eb6ac22438e17c5674345c0e3` |
| Bytes | 111,048 |
| Dimensions | 751x813 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/04292-hijab3-1.jpg |
| Capture | 2026-09-27T14:19:00+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `007_04ce6-jazz1.jpg`

| | |
|---|---|
| sha256 | `dc67c36fc734dfccd94cd66590f3d458fb3e52f426ad908d4e200bd29dcc33b8` |
| Bytes | 149,932 |
| Dimensions | 853x883 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/04ce6-jazz1.jpg |
| Capture | 2026-09-27T14:19:01+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `008_0b4c6-convo8.jpg`

| | |
|---|---|
| sha256 | `803da40a34cb00f19923f86b3e6c5635280b14101217c9f1160aa09f3b2fe2a4` |
| Bytes | 140,236 |
| Dimensions | 1281x813 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0b4c6-convo8.jpg |
| Capture | 2026-09-27T14:19:03+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `009_0c30d-rhetorical2.jpg`

| | |
|---|---|
| sha256 | `0d0b8135cbf12d15e97a13dbb5b01a75ecb58cef2eceb656822a217a1d6f245f` |
| Bytes | 47,086 |
| Dimensions | 748x169 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0c30d-rhetorical2.jpg |
| Capture | 2026-09-27T14:19:04+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `010_0c79d-salvationcritic1.jpg`

| | |
|---|---|
| sha256 | `ea0759d81c7852916c776f4167669fe853739304f4c87865a42856a259959e91` |
| Bytes | 97,381 |
| Dimensions | 930x627 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0c79d-salvationcritic1.jpg |
| Capture | 2026-09-27T14:19:05+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `011_0d072-danieltawhidi.jpg`

| | |
|---|---|
| sha256 | `354097eb4778780521bc148b6e062c7a8c932589995fe27a8a61bf4b55351cce` |
| Bytes | 140,820 |
| Dimensions | 1053x734 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0d072-danieltawhidi.jpg |
| Capture | 2026-09-27T14:19:07+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `012_0d132-danielhaya12.jpg`

| | |
|---|---|
| sha256 | `f94b66f65c91fcc42fa20a92b983251361f5c1c19197167b0e8f6d437b159ffe` |
| Bytes | 136,117 |
| Dimensions | 749x729 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0d132-danielhaya12.jpg |
| Capture | 2026-09-27T14:19:08+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `013_0edee-danielhaya15.jpg`

| | |
|---|---|
| sha256 | `1854880796a0ed9c039133fc777bc585f0aa0db57cd7e168c0e0490d5021bcfd` |
| Bytes | 158,494 |
| Dimensions | 792x784 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0edee-danielhaya15.jpg |
| Capture | 2026-09-27T14:19:09+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `014_0f451-danielhaya4.jpg`

| | |
|---|---|
| sha256 | `3ec0371111608ee29bccb7d01bc2cf8e4521f3afbbec4fa04c564ba4015f1882` |
| Bytes | 139,479 |
| Dimensions | 722x418 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/0f451-danielhaya4.jpg |
| Capture | 2026-09-27T14:19:11+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `015_1200e-symbol4.jpg`

| | |
|---|---|
| sha256 | `c8ae35391d83aedda82e64d12f60fcea1a9faac98dc6c40479c37689effa7090` |
| Bytes | 33,550 |
| Dimensions | 754x198 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1200e-symbol4.jpg |
| Capture | 2026-09-27T14:19:12+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `016_12266-dantweet1-1.jpg`

| | |
|---|---|
| sha256 | `1d2274b658f6b7f5464145df0a9bb40dab3185b8d08ba0bc19117099d7b8aed6` |
| Bytes | 104,404 |
| Dimensions | 644x594 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/12266-dantweet1-1.jpg |
| Capture | 2026-09-27T14:19:13+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `017_145dd-albanialmufrad.jpg`

| | |
|---|---|
| sha256 | `c489c002283d83cf48dc17d6a2e6975be5abf5c7fb48746562566ebe70eec32b` |
| Bytes | 14,993 |
| Dimensions | 538x116 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/145dd-albanialmufrad.jpg |
| Capture | 2026-09-27T14:19:14+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `018_16e8e-rhetorical1.jpg`

| | |
|---|---|
| sha256 | `e64c279c887d821ed56e11acbad76d5b04f922dbe0f5482dbf806e77013b9526` |
| Bytes | 179,813 |
| Dimensions | 1213x554 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/16e8e-rhetorical1.jpg |
| Capture | 2026-09-27T14:19:16+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `019_17338-daliabrennan.jpg`

| | |
|---|---|
| sha256 | `9c84704cb6ff071b71b382e9f3555d5331348d0c3e4eace04cba7d18b21c99ff` |
| Bytes | 98,772 |
| Dimensions | 1060x407 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/17338-daliabrennan.jpg |
| Capture | 2026-09-27T14:19:18+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `020_18cab-slavery1.jpg`

| | |
|---|---|
| sha256 | `77518d8357c2dd2267531c67e8a4eb6b64f19fb3d7c67ed2eb481de85cff3414` |
| Bytes | 138,480 |
| Dimensions | 1160x564 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/18cab-slavery1.jpg |
| Capture | 2026-09-27T14:19:20+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `021_19229-gouda.jpg`

| | |
|---|---|
| sha256 | `bcea44bd9c68e920ba38abada4c3484eee8d00a545e06ecf52e56dee72ec479f` |
| Bytes | 77,528 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/19229-gouda.jpg |
| Capture | 2026-09-27T14:19:21+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `022_19feb-convo1.jpg`

| | |
|---|---|
| sha256 | `0b22219d71bda11901d0e83a1e0bdf6d9ea4b90c20f23a8060d87479b63c2344` |
| Bytes | 215,054 |
| Dimensions | 1250x759 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/19feb-convo1.jpg |
| Capture | 2026-09-27T14:19:23+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `023_1a640-fiqhhuman6.jpg`

| | |
|---|---|
| sha256 | `58e14eb9a61095c4a93a1eb0588495a264882135f132c820a05ec845bb9e00db` |
| Bytes | 220,596 |
| Dimensions | 742x738 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1a640-fiqhhuman6.jpg |
| Capture | 2026-09-27T14:19:24+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `024_1ab5e-evo7.jpg`

| | |
|---|---|
| sha256 | `6ba463c1f174c3c1bcbc7d341a6ef24fa01b54d14ff6f7d216c2388e0fbc844b` |
| Bytes | 314,605 |
| Dimensions | 1120x962 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1ab5e-evo7.jpg |
| Capture | 2026-09-27T14:19:26+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `025_1b171-readinglist.jpg`

| | |
|---|---|
| sha256 | `f69bd42a0626083033aad050dd8fae2debf37be5d17d44d7a97ef4cdeb020efe` |
| Bytes | 73,853 |
| Dimensions | 1107x595 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1b171-readinglist.jpg |
| Capture | 2026-09-27T14:19:27+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `026_1b3e1-dalia13.jpg`

| | |
|---|---|
| sha256 | `7e9fba9ba07eec86990ed724a448f6c4247b41451544117580d464ff3c689923` |
| Bytes | 297,472 |
| Dimensions | 950x1030 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1b3e1-dalia13.jpg |
| Capture | 2026-09-27T14:19:28+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `027_1b541-9.jpg`

| | |
|---|---|
| sha256 | `982a26f151a87f615a7a6178c9a0eb0207f2146f65197a657916e0c2a4c641bf` |
| Bytes | 159,163 |
| Dimensions | 760x578 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1b541-9.jpg |
| Capture | 2026-09-27T14:19:29+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `028_1c755-danielhaya13.jpg`

| | |
|---|---|
| sha256 | `63e23c083c13ff434e0283621f38d49a24b0a264638b6a1ee3e70012810937ee` |
| Bytes | 187,638 |
| Dimensions | 1297x897 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1c755-danielhaya13.jpg |
| Capture | 2026-09-27T14:19:31+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `029_1cbf8-cpost1.jpg`

| | |
|---|---|
| sha256 | `30ba47e0041dd13ba958966ec535ed141884834409cf23c8f06ddd38de2781a4` |
| Bytes | 222,073 |
| Dimensions | 796x1139 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1cbf8-cpost1.jpg |
| Capture | 2026-09-27T14:19:32+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `030_1f0f3-evo10.jpg`

| | |
|---|---|
| sha256 | `c50814e300d743010d32d04aed6aa51b26a660fc7f05e7e6db2b1eb0160b98b7` |
| Bytes | 206,113 |
| Dimensions | 1120x653 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1f0f3-evo10.jpg |
| Capture | 2026-09-27T14:19:34+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `031_1fb46-wala2.jpg`

| | |
|---|---|
| sha256 | `b040427ffca553dfef6ef1e1c1c03ddd29dd96c29422ad5583ba5050e9427287` |
| Bytes | 241,491 |
| Dimensions | 1138x861 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1fb46-wala2.jpg |
| Capture | 2026-09-27T14:19:36+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `032_1fd6f-wala3.jpg`

| | |
|---|---|
| sha256 | `6dc6b24dccdf1286117a05df9a41cfe1df425b098aba4f39e8dbcc4c650b9dc6` |
| Bytes | 126,792 |
| Dimensions | 1138x342 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1fd6f-wala3.jpg |
| Capture | 2026-09-27T14:19:37+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `033_1ffdc-evo9.jpg`

| | |
|---|---|
| sha256 | `5bef058eaf968f43436b1eed8125a92504b803788803875c7875afc5892dc917` |
| Bytes | 245,479 |
| Dimensions | 1120x702 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/1ffdc-evo9.jpg |
| Capture | 2026-09-27T14:19:38+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `034_203bf-evo12.jpg`

| | |
|---|---|
| sha256 | `8912598b86500476e07b37ae45d6423941ca13a3f2849d1a4171d06f173abee2` |
| Bytes | 147,598 |
| Dimensions | 1120x473 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/203bf-evo12.jpg |
| Capture | 2026-09-27T14:19:40+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `035_20475-errex1.5.jpg`

| | |
|---|---|
| sha256 | `9521e3a8918c73caabd2792d29c8861a871bb1184d245770dc0be5bb8e48d415` |
| Bytes | 207,863 |
| Dimensions | 909x705 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/20475-errex1.5.jpg |
| Capture | 2026-09-27T14:19:42+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `036_204cb-convo2.jpg`

| | |
|---|---|
| sha256 | `9639c29bb43ac1580a286ade4b6b13c9c8a1bac83460051fcfb58a5acbf551d3` |
| Bytes | 163,719 |
| Dimensions | 1268x765 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/204cb-convo2.jpg |
| Capture | 2026-09-27T14:19:43+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `038_26d75-neversaid.jpg`

| | |
|---|---|
| sha256 | `d10f2f0ae5fdd91e87cffeecf060230ddadb2a91b4977e634c5a898a2bc25219` |
| Bytes | 11,858 |
| Dimensions | 749x74 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/26d75-neversaid.jpg |
| Capture | 2026-09-27T14:19:45+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `039_28ff6-mythical1.jpg`

| | |
|---|---|
| sha256 | `15d9d6d51dca3c9689d766cc5c77d38399f97d13a521dddd014b9d142d98e7fb` |
| Bytes | 105,180 |
| Dimensions | 1092x296 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/28ff6-mythical1.jpg |
| Capture | 2026-09-27T14:19:47+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `040_2b29e-salvation8.jpg`

| | |
|---|---|
| sha256 | `a0f217ab13aa8bfefc7510b6c1eb2f98e355403bae0eeabbcd61dba9335794c0` |
| Bytes | 155,633 |
| Dimensions | 864x491 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2b29e-salvation8.jpg |
| Capture | 2026-09-27T14:19:49+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `041_2d377-slavery5.jpg`

| | |
|---|---|
| sha256 | `a05f82a6a16dbb352a0b677945608e64982209a642f7f35ececf8c6af00eee1f` |
| Bytes | 109,889 |
| Dimensions | 1138x512 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2d377-slavery5.jpg |
| Capture | 2026-09-27T14:19:50+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `042_2dc23-musa1.jpg`

| | |
|---|---|
| sha256 | `e7392516732d017abc73398d61cec916ae346d9df98c3867193068b112b818e4` |
| Bytes | 196,237 |
| Dimensions | 1883x755 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2dc23-musa1.jpg |
| Capture | 2026-09-27T14:19:52+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `043_2dd91-wise.jpg`

| | |
|---|---|
| sha256 | `b666fff2ad1b228c7500d00d32255163f81d873dcfe43d589949bfde8867d146` |
| Bytes | 196,852 |
| Dimensions | 869x888 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2dd91-wise.jpg |
| Capture | 2026-09-27T14:19:53+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `044_2e516-beat4.jpg`

| | |
|---|---|
| sha256 | `5081351e54c81058a2935b0f9970060b3040ee70a699b8d320a15fcd62bbce07` |
| Bytes | 53,689 |
| Dimensions | 773x301 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2e516-beat4.jpg |
| Capture | 2026-09-27T14:19:54+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `045_2e822-salvation3.5.jpg`

| | |
|---|---|
| sha256 | `e9be661a59fcacbbb0799b5dbed8cba4fa73f073d076f97d05445e18e6ad37ed` |
| Bytes | 142,825 |
| Dimensions | 864x453 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2e822-salvation3.5.jpg |
| Capture | 2026-09-27T14:19:56+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `046_2ffde-dhcover3.jpg`

| | |
|---|---|
| sha256 | `8087baec64e6501439e47efbb08c8c030f5ceb765006c5b48f8e9f996064fe1e` |
| Bytes | 167,394 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/2ffde-dhcover3.jpg |
| Capture | 2026-09-27T14:19:57+05:30 |
| Role in the post | `featured_media` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | The review's cover image: a cut-out photograph of Daniel Haqiqatjou placed before a windmill whose base is graffitied with the word “Yaqeen” and the label “the convict”. |
| Alt text basis | written after viewing the image |

### `047_30896-daliagallup.jpg`

| | |
|---|---|
| sha256 | `03bacfe0fc7e08b8b1c92dad73dec76583b6fd37478ecf32df62f364a3264ba9` |
| Bytes | 219,166 |
| Dimensions | 910x660 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/30896-daliagallup.jpg |
| Capture | 2026-09-27T14:19:59+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `048_312e5-hijab5-1.jpg`

| | |
|---|---|
| sha256 | `0245482745f1e706dda5bae7ac3761195be02c52e28dde929f821412fcc29efd` |
| Bytes | 116,960 |
| Dimensions | 673x653 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/312e5-hijab5-1.jpg |
| Capture | 2026-09-27T14:20:00+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `049_312f2-evo11.jpg`

| | |
|---|---|
| sha256 | `00d023b75dc07f9842473c87ce68674631b2e13cb757b371143147e7bf8dea2f` |
| Bytes | 160,403 |
| Dimensions | 1120x551 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/312f2-evo11.jpg |
| Capture | 2026-09-27T14:20:01+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `050_33a65-danielglances.jpg`

| | |
|---|---|
| sha256 | `c17eab3736b0985e1f5f6635e39988b05fd28120da9d5bc6282f61be93e66159` |
| Bytes | 152,468 |
| Dimensions | 1281x820 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/33a65-danielglances.jpg |
| Capture | 2026-09-27T14:20:03+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | YouTube screenshot of 'Is Feminism Dangerous? A Muslim Deconstruction': a woman in a hijab and the speaker at a lecture table. |
| Alt text basis | written after viewing the image |

### `051_33cab-8.5.jpg`

| | |
|---|---|
| sha256 | `dd1a5928903ae0fa612cb47aff04bdffd4fe62d8f87d2f9cc3789f715c75135c` |
| Bytes | 119,470 |
| Dimensions | 833x492 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/33cab-8.5.jpg |
| Capture | 2026-09-27T14:20:05+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `052_35a9e-evosummary.jpg`

| | |
|---|---|
| sha256 | `1b3a921b2ace04f9181c885b3347abd6e38478d12b48dff0737a3d931fc9beaf` |
| Bytes | 246,702 |
| Dimensions | 1095x791 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/35a9e-evosummary.jpg |
| Capture | 2026-09-27T14:20:06+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `054_371c0-danielhaya1-2.jpg`

| | |
|---|---|
| sha256 | `95e2b4b8d7ca9b00d9a177cf9762f3c2d6024d11c411b26dac72f258c266120d` |
| Bytes | 179,465 |
| Dimensions | 1013x660 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/371c0-danielhaya1-2.jpg |
| Capture | 2026-09-27T14:20:09+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of a Facebook post by Daniel Haqiqatjou about prayer during menstruation, with replies. |
| Alt text basis | written after viewing the image |

### `055_386b1-danielhaya18.jpg`

| | |
|---|---|
| sha256 | `7525d0638273d4524c1859e27955140d2d3c0b856822b7e5d8f66a196d64d52b` |
| Bytes | 85,107 |
| Dimensions | 703x842 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/386b1-danielhaya18.jpg |
| Capture | 2026-09-27T14:20:10+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `056_392fe-dalia10.jpg`

| | |
|---|---|
| sha256 | `a572c59fb069cffed12c5d207ddb8c55ed35e0cb80ff83d69f57eb05251a6e11` |
| Bytes | 138,542 |
| Dimensions | 970x512 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/392fe-dalia10.jpg |
| Capture | 2026-09-27T14:20:11+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `057_39a4e-modeltitle3.jpg`

| | |
|---|---|
| sha256 | `0f6e1f2b44dd4b025ee01496557aa2a31617e2df3033a6b7b76ebc15065295aa` |
| Bytes | 136,129 |
| Dimensions | 764x934 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/39a4e-modeltitle3.jpg |
| Capture | 2026-09-27T14:20:13+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `058_3abbc-unseenarabic.jpg`

| | |
|---|---|
| sha256 | `77f415524972bcf5fc31b96b827b058f2b35e142af06994da968ff6204e6994e` |
| Bytes | 48,218 |
| Dimensions | 1380x251 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/3abbc-unseenarabic.jpg |
| Capture | 2026-09-27T14:20:15+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `059_3bd95-dandaliafb.jpg`

| | |
|---|---|
| sha256 | `8fb567d34b64b378ed2a2aaa8a26f506d08e7d3a40b6336840505973745f2877` |
| Bytes | 96,855 |
| Dimensions | 777x502 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/3bd95-dandaliafb.jpg |
| Capture | 2026-09-27T14:20:16+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `060_3dc3d-jazzvideodate.jpg`

| | |
|---|---|
| sha256 | `673d2e586fed3f7f800ce3ea75ee24092ec4bb70d31ef98ccd18ac9dd02ee449` |
| Bytes | 97,375 |
| Dimensions | 1424x523 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/3dc3d-jazzvideodate.jpg |
| Capture | 2026-09-27T14:20:17+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `061_3df3c-dalia6.jpg`

| | |
|---|---|
| sha256 | `564ac9810c2762de744faa195212ddf4bf753e6b806a141af6b0f70f0b5a917a` |
| Bytes | 222,637 |
| Dimensions | 942x802 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/3df3c-dalia6.jpg |
| Capture | 2026-09-27T14:20:19+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `062_3ef70-2.png`

| | |
|---|---|
| sha256 | `67cd1d6aadcb8ed8099137184f235f4781ef1b1dd7bffb8c97bf1a75b5e3423b` |
| Bytes | 35,347 |
| Dimensions | 735x851 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/3ef70-2.png |
| Capture | 2026-09-27T14:20:21+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `064_3ffa8-fiqhhuman8.jpg`

| | |
|---|---|
| sha256 | `c52188aeec69c9eec947c16264c4776fe7f7abae0a204db9d38776e0b1714ea8` |
| Bytes | 235,829 |
| Dimensions | 735x744 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/3ffa8-fiqhhuman8.jpg |
| Capture | 2026-09-27T14:20:24+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `065_40946-eq3.jpg`

| | |
|---|---|
| sha256 | `608fb5e355c46692ad724f78714c3af6306d0320c762bc93313d308ba84073f7` |
| Bytes | 29,865 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/40946-eq3.jpg |
| Capture | 2026-09-27T14:20:25+05:30 |
| Role in the post | `img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `066_43db7-danieltweet1.jpg`

| | |
|---|---|
| sha256 | `35925eff0e1bb9aae49856a5f07008dfa4f1c547f588ec520cc0c8531e9c3912` |
| Bytes | 47,225 |
| Dimensions | 687x405 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/43db7-danieltweet1.jpg |
| Capture | 2026-09-27T14:20:26+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `067_4459d-moad.jpg`

| | |
|---|---|
| sha256 | `8ab7562fd8117901af0dabd613df4987bcf3d33d013c95eebdd5b6643c6ebd65` |
| Bytes | 190,316 |
| Dimensions | 887x602 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4459d-moad.jpg |
| Capture | 2026-09-27T14:20:27+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `068_45bae-racism2.jpg`

| | |
|---|---|
| sha256 | `36a4a7c9e1e050b0a67a5cfe2a471160fa311334bd8c22ec08ee71f398d3d51c` |
| Bytes | 230,023 |
| Dimensions | 976x798 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/45bae-racism2.jpg |
| Capture | 2026-09-27T14:20:29+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `069_476e3-salvation5.jpg`

| | |
|---|---|
| sha256 | `31c50cba4b2da8630e0aadd1743a635d32405c97f7d3b0912ab01d50f9ec8e3b` |
| Bytes | 167,297 |
| Dimensions | 864x562 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/476e3-salvation5.jpg |
| Capture | 2026-09-27T14:20:30+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `070_48a57-symbol9.jpg`

| | |
|---|---|
| sha256 | `7cd315a3b346258411cb408d71722ba20f2deeee8ca225aef82f6d06521d6128` |
| Bytes | 190,765 |
| Dimensions | 794x603 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/48a57-symbol9.jpg |
| Capture | 2026-09-27T14:20:32+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `071_48df9-salvation1.jpg`

| | |
|---|---|
| sha256 | `be8b32a4db8a7ae2354667dd617ef131b3697a43aa0916ee285c553b1025adce` |
| Bytes | 145,435 |
| Dimensions | 982x594 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/48df9-salvation1.jpg |
| Capture | 2026-09-27T14:20:33+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `072_4940c-symbol12.jpg`

| | |
|---|---|
| sha256 | `f3b091f44ec40552f5841a4ccaec100bdb37376bc48c03e8b1801588b0e53d9d` |
| Bytes | 139,473 |
| Dimensions | 794x471 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4940c-symbol12.jpg |
| Capture | 2026-09-27T14:20:35+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `074_4a245-counter5.jpg`

| | |
|---|---|
| sha256 | `3bcb2a5c4f18d6c9edcebb290c4835f1aef06ff9b81fdd35666b8ec6bb8d0677` |
| Bytes | 167,140 |
| Dimensions | 950x500 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4a245-counter5.jpg |
| Capture | 2026-09-27T14:20:38+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `075_4a451-danielhaya19.jpg`

| | |
|---|---|
| sha256 | `c6ff07e406c46241d47973bc3a2e7be1848db547cf73287d47e215c9bc079ca9` |
| Bytes | 93,790 |
| Dimensions | 852x758 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4a451-danielhaya19.jpg |
| Capture | 2026-09-27T14:20:39+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `076_4a612-errex5.jpg`

| | |
|---|---|
| sha256 | `5a0cf008ee9d09841cb8b50e265d40ee08d35f1ed310676256928e0f929ba764` |
| Bytes | 270,724 |
| Dimensions | 852x770 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4a612-errex5.jpg |
| Capture | 2026-09-27T14:20:41+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `077_4a878-evoresponse-1.jpg`

| | |
|---|---|
| sha256 | `819807b5595eb59c39fe36dd686c408ac21c535dd60bc56845bfe0e4678af7cd` |
| Bytes | 145,717 |
| Dimensions | 958x502 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4a878-evoresponse-1.jpg |
| Capture | 2026-09-27T14:20:42+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `078_4c8c2-danielhaya20.jpg`

| | |
|---|---|
| sha256 | `2bdf394db850c6f3a022bb9b3d4173f90457a8e7a632d7fb6ee4caa2e9ad8ebf` |
| Bytes | 155,242 |
| Dimensions | 703x842 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4c8c2-danielhaya20.jpg |
| Capture | 2026-09-27T14:20:43+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `079_4db6d-dalia.jpg`

| | |
|---|---|
| sha256 | `4d6896813d146287caf124394394e93c799b2698b548691cf1c723d9f7989eab` |
| Bytes | 152,994 |
| Dimensions | 958x717 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4db6d-dalia.jpg |
| Capture | 2026-09-27T14:20:45+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `080_4df1d-danielhaya3.jpg`

| | |
|---|---|
| sha256 | `5b2dcb788008dfb9970a998760e4a3d81c61902611b61afe80d3f804a9e2126a` |
| Bytes | 156,237 |
| Dimensions | 722x786 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4df1d-danielhaya3.jpg |
| Capture | 2026-09-27T14:20:46+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `081_4ecda-update1.jpg`

| | |
|---|---|
| sha256 | `591638f172d8e417f2a0690e41d645fa57fc223e9d9b3257cb08352fbded6f1b` |
| Bytes | 378,379 |
| Dimensions | 1478x1378 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4ecda-update1.jpg |
| Capture | 2026-09-27T14:20:48+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `082_4f233-eq1.jpg`

| | |
|---|---|
| sha256 | `647c2b6e3a3543c8791cf90991616a49f9909f020623a3f735dff14e8ebd7fcf` |
| Bytes | 50,640 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4f233-eq1.jpg |
| Capture | 2026-09-27T14:20:49+05:30 |
| Role in the post | `img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `083_50365-convo4.jpg`

| | |
|---|---|
| sha256 | `86e78a1b37bc8a55bcbae9a939e07e3ccaaea26f9584da511e8a9f984d88f9ff` |
| Bytes | 130,294 |
| Dimensions | 976x799 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/50365-convo4.jpg |
| Capture | 2026-09-27T14:20:50+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `084_51319-rosa1.jpg`

| | |
|---|---|
| sha256 | `6f2c1116850e625c2b35db50552ff56343cb81ce2ec52166b18f34a87b694efe` |
| Bytes | 114,575 |
| Dimensions | 832x741 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/51319-rosa1.jpg |
| Capture | 2026-09-27T14:20:51+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `085_51eb9-danielhaya5.jpg`

| | |
|---|---|
| sha256 | `00352f27055d81ec527f8ebf5bf3bc2e46b23d1982231f17d1d94a7c45d7be61` |
| Bytes | 72,141 |
| Dimensions | 665x503 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/51eb9-danielhaya5.jpg |
| Capture | 2026-09-27T14:20:52+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `086_52caa-7.jpg`

| | |
|---|---|
| sha256 | `4206eb9825ceccd64c5363695b1b2546f7ccf8eb66045bfa9ccd30c1a264513c` |
| Bytes | 182,613 |
| Dimensions | 755x747 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/52caa-7.jpg |
| Capture | 2026-09-27T14:20:54+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `087_53b0c-dalia2.jpg`

| | |
|---|---|
| sha256 | `73d1f0c1dea8fedf3568d9fe0f071f682c4f45b602225d829ebe91507cbc156b` |
| Bytes | 140,708 |
| Dimensions | 937x469 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/53b0c-dalia2.jpg |
| Capture | 2026-09-27T14:20:55+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `088_53b4a-fiqhhuman3.jpg`

| | |
|---|---|
| sha256 | `ee17ba0321c7217c06a4315288689ccb7f811fb085a43aa3f8c3f762bc001b54` |
| Bytes | 178,188 |
| Dimensions | 833x653 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/53b4a-fiqhhuman3.jpg |
| Capture | 2026-09-27T14:20:57+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `089_55903-photo-2020-08-10-09-10-01.jpg`

| | |
|---|---|
| sha256 | `ac8fecd5398a86b0c7bd2764fa910d2b9ce773ec474d614db4692d9317b71d71` |
| Bytes | 287,378 |
| Dimensions | 1600x1030 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/55903-photo-2020-08-10-09-10-01.jpg |
| Capture | 2026-09-27T14:20:58+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of the Muslim Matters article 'Questions About My Political Activism' by Imam Omar Suleiman. |
| Alt text basis | written after viewing the image |

### `090_56258-hijab9.5.jpg`

| | |
|---|---|
| sha256 | `8aaf53b6e56907cff5e190b33c427807f1cc110ce2fabb2fd836d7890d1eeaac` |
| Bytes | 108,415 |
| Dimensions | 1118x810 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/56258-hijab9.5.jpg |
| Capture | 2026-09-27T14:21:00+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `091_588c4-hijab4-1.jpg`

| | |
|---|---|
| sha256 | `9fe5d3316cefd39127cd8bb79cd9e89659a44a7cdc9a48d0fa0a27626eb5cd69` |
| Bytes | 134,298 |
| Dimensions | 671x955 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/588c4-hijab4-1.jpg |
| Capture | 2026-09-27T14:21:02+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `092_59206-11.jpg`

| | |
|---|---|
| sha256 | `6ad4f0621d4901e80385e24c098bc4ed11a65e4d970eb16958406fed3e80eb4d` |
| Bytes | 218,871 |
| Dimensions | 815x799 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/59206-11.jpg |
| Capture | 2026-09-27T14:21:03+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `093_59710-slavery4.jpg`

| | |
|---|---|
| sha256 | `f3f0e2b088fc05f17750df478380ee2b07246f3052833fee53d4659f279982b5` |
| Bytes | 334,784 |
| Dimensions | 1138x932 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/59710-slavery4.jpg |
| Capture | 2026-09-27T14:21:04+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `094_5a188-hijab2-1.jpg`

| | |
|---|---|
| sha256 | `8ee38e0da119bf4e9596f2aca4722b0fa9eea981e809790951e041f5fff1df13` |
| Bytes | 133,467 |
| Dimensions | 611x867 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5a188-hijab2-1.jpg |
| Capture | 2026-09-27T14:21:05+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `095_5b0dc-rameez.jpg`

| | |
|---|---|
| sha256 | `dc4730661cb93327dc527a6a967c23218770fd76a2caa3d23cf8a7b0b937ef24` |
| Bytes | 251,825 |
| Dimensions | 804x820 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5b0dc-rameez.jpg |
| Capture | 2026-09-27T14:21:07+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of a public Facebook post by Rameez Abid comparing a Yaqeen Institute paper with Daniel Haqiqatjou's critique. |
| Alt text basis | written after viewing the image |

### `096_5c418-fiqhhuman5.jpg`

| | |
|---|---|
| sha256 | `6da042068d9125abfb7970821481c4ec9c2fd390939cae1396c9af8142ce0d1e` |
| Bytes | 314,533 |
| Dimensions | 742x1052 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5c418-fiqhhuman5.jpg |
| Capture | 2026-09-27T14:21:09+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `097_5c98b-unseenarabic2.jpg`

| | |
|---|---|
| sha256 | `91b29aa74cd7db712d270c2cf31f8f50dc7e4fcfb8f39efcc2e7f10230ffc4eb` |
| Bytes | 41,289 |
| Dimensions | 1482x185 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5c98b-unseenarabic2.jpg |
| Capture | 2026-09-27T14:21:10+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `098_5cffc-beat3-e1596677224874.jpg`

| | |
|---|---|
| sha256 | `efc4df62e299f95ae164626b4ef88de37714f7853e443e500e0433c6befcac37` |
| Bytes | 53,266 |
| Dimensions | 771x464 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5cffc-beat3-e1596677224874.jpg |
| Capture | 2026-09-27T14:21:11+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `099_5dfdf-hr1.jpg`

| | |
|---|---|
| sha256 | `c664ee0a9a7db7cd5ac5bce642d6430d418cd1e9a168ad4f5ed67280a24097c5` |
| Bytes | 205,244 |
| Dimensions | 818x712 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5dfdf-hr1.jpg |
| Capture | 2026-09-27T14:21:13+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `100_5e0a4-aisha1.jpg`

| | |
|---|---|
| sha256 | `a1f2847bbaa062470bfcd1b987574d077541677677e47541bca37216bf4df038` |
| Bytes | 266,017 |
| Dimensions | 1138x734 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5e0a4-aisha1.jpg |
| Capture | 2026-09-27T14:21:14+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `101_5e6d3-8.7.jpg`

| | |
|---|---|
| sha256 | `9033038fd1afd24719e88d7647ad07a114751fdda1cee08ec97ef1995cc41d8e` |
| Bytes | 75,434 |
| Dimensions | 786x325 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5e6d3-8.7.jpg |
| Capture | 2026-09-27T14:21:15+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `102_5fe2f-ilhanpraise.jpg`

| | |
|---|---|
| sha256 | `3d70a07de6ba387f4b4b68b99876cff56e195a0b634d7036223b03a4509b4c76` |
| Bytes | 103,246 |
| Dimensions | 510x968 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5fe2f-ilhanpraise.jpg |
| Capture | 2026-09-27T14:21:17+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `103_60775-dalia9.jpg`

| | |
|---|---|
| sha256 | `bb5b23f966e97150dce73a541429dc2eda7143f5db63602781b4b9684d097a9c` |
| Bytes | 141,987 |
| Dimensions | 942x404 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/60775-dalia9.jpg |
| Capture | 2026-09-27T14:21:18+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `104_608e3-danielhaya7.jpg`

| | |
|---|---|
| sha256 | `14fb602db029d91eb69c0213ab9cd2812c2de19e2047b77f84995de5915d1759` |
| Bytes | 114,472 |
| Dimensions | 789x832 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/608e3-danielhaya7.jpg |
| Capture | 2026-09-27T14:21:19+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `105_628df-jazz2.jpg`

| | |
|---|---|
| sha256 | `727d1498c0942317192a600b9f8529555597384ce467147a76bc5cc1380b6355` |
| Bytes | 137,863 |
| Dimensions | 810x450 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/628df-jazz2.jpg |
| Capture | 2026-09-27T14:21:21+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `106_63f14-danielhaya16.jpg`

| | |
|---|---|
| sha256 | `f430b32f7f17794eeabcb8edd9c2c6fd13db84b560cd99ccf8c239c22ba157bd` |
| Bytes | 157,972 |
| Dimensions | 828x858 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/63f14-danielhaya16.jpg |
| Capture | 2026-09-27T14:21:23+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `108_64930-aishaage2.jpg`

| | |
|---|---|
| sha256 | `d43984b7bf28fede4b2ca6d98b7271f3c4c7d1aeb5c2a6703c889d7eca8ccba6` |
| Bytes | 270,067 |
| Dimensions | 1832x900 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/64930-aishaage2.jpg |
| Capture | 2026-09-27T14:21:26+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `109_6883e-hijab7-1.jpg`

| | |
|---|---|
| sha256 | `12af7faf5a61367258560d6b77695473cbe921888a221f7089c0f95412fd40f6` |
| Bytes | 112,319 |
| Dimensions | 651x675 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/6883e-hijab7-1.jpg |
| Capture | 2026-09-27T14:21:27+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `110_68da4-danielhaya11.jpg`

| | |
|---|---|
| sha256 | `c58c59d1ea1e3676f02ef5debd2b30cdf079975fe8250253af30cb529ea0664f` |
| Bytes | 168,140 |
| Dimensions | 700x856 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/68da4-danielhaya11.jpg |
| Capture | 2026-09-27T14:21:30+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `111_6af76-evo5new.jpg`

| | |
|---|---|
| sha256 | `55f055cdbc26c2908edde52bc9bb0c15a35e1366165265d90949c2e7e2bef25e` |
| Bytes | 381,056 |
| Dimensions | 1154x1082 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/6af76-evo5new.jpg |
| Capture | 2026-09-27T14:21:31+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `112_6c157-wala1.jpg`

| | |
|---|---|
| sha256 | `2548e615f0425be35dd27412e1289f0f2e81871cd32ac1344ddddfe07d649630` |
| Bytes | 286,440 |
| Dimensions | 1138x854 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/6c157-wala1.jpg |
| Capture | 2026-09-27T14:21:33+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `113_6f368-orientalistseditors1.jpg`

| | |
|---|---|
| sha256 | `d8a3e358eb6cacc89fa5e214910ffb4295b7895aa9135e521cba51df9fb3c807` |
| Bytes | 50,765 |
| Dimensions | 877x876 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/6f368-orientalistseditors1.jpg |
| Capture | 2026-09-27T14:21:34+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `114_6f9cc-dalia3.jpg`

| | |
|---|---|
| sha256 | `50bfadfe97957c5f118bc3b89ef94198fa79c757a279c79307404947b5f20d8a` |
| Bytes | 173,535 |
| Dimensions | 879x842 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/6f9cc-dalia3.jpg |
| Capture | 2026-09-27T14:21:35+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `115_715da-errex6.5.jpg`

| | |
|---|---|
| sha256 | `b2f29115655a81846d62234632fb172c61e181d7f0086cec94c43b43fd6fe0d8` |
| Bytes | 177,457 |
| Dimensions | 971x770 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/715da-errex6.5.jpg |
| Capture | 2026-09-27T14:21:37+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `116_71e40-6.png`

| | |
|---|---|
| sha256 | `57af49da85d1150292f0ce41275b6442ce9d52053e64ecfaa096216848ac34ef` |
| Bytes | 23,454 |
| Dimensions | 742x396 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/71e40-6.png |
| Capture | 2026-09-27T14:21:38+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `117_7278e-symbol10.jpg`

| | |
|---|---|
| sha256 | `3981fe47ce18300bd87ec0fddead830a925ab8dbf65fc0b6cf109ca4c131f3c9` |
| Bytes | 252,820 |
| Dimensions | 794x822 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/7278e-symbol10.jpg |
| Capture | 2026-09-27T14:21:39+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `118_735d0-hijab9-1.jpg`

| | |
|---|---|
| sha256 | `37c5c52b2b0a7d4d6bc5c4f884fcc9249e35a777c09a41573412e5a1d8290f49` |
| Bytes | 107,571 |
| Dimensions | 693x645 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/735d0-hijab9-1.jpg |
| Capture | 2026-09-27T14:21:41+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `119_75812-readinglist1.jpg`

| | |
|---|---|
| sha256 | `9295e5661d34dbc7143c19c4242e826020382ae615c20b7c164d4425d5ae2419` |
| Bytes | 209,045 |
| Dimensions | 1526x640 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/75812-readinglist1.jpg |
| Capture | 2026-09-27T14:21:42+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `120_758c1-slavery2.jpg`

| | |
|---|---|
| sha256 | `eb9be2fa0682fc2e39dd17bd1b4f88d89be38231e51ea0997df5800b6a1d8cd2` |
| Bytes | 30,965 |
| Dimensions | 1138x244 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/758c1-slavery2.jpg |
| Capture | 2026-09-27T14:21:43+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `122_775d7-eq2.jpg`

| | |
|---|---|
| sha256 | `99ca47c37559944bdaf112d3e68ef3a6fefec1a739e3cfaba5d3b16ae0fe9937` |
| Bytes | 45,613 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/775d7-eq2.jpg |
| Capture | 2026-09-27T14:21:46+05:30 |
| Role in the post | `img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `123_77c30-formatex.jpg`

| | |
|---|---|
| sha256 | `fc2ad6b86015e6a6d14b49180ffc8810f64b3da6bffafeb1be69ba6091592baa` |
| Bytes | 125,886 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/77c30-formatex.jpg |
| Capture | 2026-09-27T14:21:48+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `124_7a751-khansakhsi.jpg`

| | |
|---|---|
| sha256 | `9f4f63d9e19925a9868264c878bc3b1b723738334bce9046ac1d4377e5c20d29` |
| Bytes | 252,474 |
| Dimensions | 838x848 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/7a751-khansakhsi.jpg |
| Capture | 2026-09-27T14:21:49+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Page from a fiqh work quoting al-Sarakhsi on jurists historicising the rulings of their predecessors, with footnotes 110-111. |
| Alt text basis | written after viewing the image |

### `125_7b453-nazirslavery1.jpg`

| | |
|---|---|
| sha256 | `62e11a7298d6501f8bed7072b24bfa0aae8ff0fb94bd000629e87f502e8baf06` |
| Bytes | 284,706 |
| Dimensions | 893x649 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/7b453-nazirslavery1.jpg |
| Capture | 2026-09-27T14:21:51+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `126_7c750-wala5.jpg`

| | |
|---|---|
| sha256 | `d420de8005a530af0223878b3c74fb5481ba6fe21874997e746a8e915e71d25e` |
| Bytes | 104,465 |
| Dimensions | 935x293 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/7c750-wala5.jpg |
| Capture | 2026-09-27T14:21:52+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `127_7cb1a-danielhaya8.jpg`

| | |
|---|---|
| sha256 | `736f6637039d9c43d8fce16b2a6cf2b5c4494e13e23ff1abc38684fd540cc8ef` |
| Bytes | 124,061 |
| Dimensions | 752x753 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/7cb1a-danielhaya8.jpg |
| Capture | 2026-09-27T14:21:54+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `129_7ead3-beat1.jpg`

| | |
|---|---|
| sha256 | `56d168ee176ffc67fc799159f2ece09b40b66ea646740069247a6e1c4f0cacc1` |
| Bytes | 255,363 |
| Dimensions | 785x933 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/7ead3-beat1.jpg |
| Capture | 2026-09-27T14:21:56+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `130_80e9c-danielhaya10.jpg`

| | |
|---|---|
| sha256 | `4e9c92b3a75fa52c788e993632d75c03ae0c157b01a515d39ebb124a34275dea` |
| Bytes | 130,668 |
| Dimensions | 672x777 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/80e9c-danielhaya10.jpg |
| Capture | 2026-09-27T14:21:57+05:30 |
| Role in the post | `img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `131_8379b-salvation4.8.jpg`

| | |
|---|---|
| sha256 | `217618e2d68d067398a891ab05eda06b1ba56860d84b03579221096a73f2d03c` |
| Bytes | 148,693 |
| Dimensions | 847x487 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/8379b-salvation4.8.jpg |
| Capture | 2026-09-27T14:21:59+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `132_83f79-salvationcritic4.jpg`

| | |
|---|---|
| sha256 | `104684d02900a70e43d7c7bb169d8daa4d7d7e8580f2f7b07e68d5d3460ff0a6` |
| Bytes | 185,264 |
| Dimensions | 714x784 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/83f79-salvationcritic4.jpg |
| Capture | 2026-09-27T14:22:00+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `133_8486e-errex1.jpg`

| | |
|---|---|
| sha256 | `be13f78f00268fadc423496c25969897b5d81765314f6eca5518b9b2a8f5354e` |
| Bytes | 167,639 |
| Dimensions | 761x610 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/8486e-errex1.jpg |
| Capture | 2026-09-27T14:22:02+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `134_8568c-evo6.jpg`

| | |
|---|---|
| sha256 | `3dd6b066df70e9006ece1fb2c7034764f40b279010cbdd443dd253cda6918680` |
| Bytes | 215,658 |
| Dimensions | 1154x673 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/8568c-evo6.jpg |
| Capture | 2026-09-27T14:22:03+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `135_871a6-salvation3.jpg`

| | |
|---|---|
| sha256 | `7c02213b4007caa5495cbeb738e9ba47028ebe98378fdbe0253982ffc62879bd` |
| Bytes | 283,337 |
| Dimensions | 922x971 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/871a6-salvation3.jpg |
| Capture | 2026-09-27T14:22:05+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `138_8bddc-dalia7.jpg`

| | |
|---|---|
| sha256 | `f0fb5d7512fe885d1630bfb7196b77b816aad0f5721cb3c1b6912bc576256bb3` |
| Bytes | 180,531 |
| Dimensions | 942x602 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/8bddc-dalia7.jpg |
| Capture | 2026-09-27T14:22:09+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `139_8dfa6-wise2.jpg`

| | |
|---|---|
| sha256 | `91e58b32ae7e4feabc650d6b53597e002ce474e6209d93ac6ad1fdaa5139a34a` |
| Bytes | 50,923 |
| Dimensions | 795x430 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/8dfa6-wise2.jpg |
| Capture | 2026-09-27T14:22:10+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `140_913b4-racism1.jpg`

| | |
|---|---|
| sha256 | `7481f5df947747955758a9fdcbc1af85818f1f620a56a4db095b4278e07228a5` |
| Bytes | 166,265 |
| Dimensions | 961x681 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/913b4-racism1.jpg |
| Capture | 2026-09-27T14:22:11+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `143_939fc-rosa3.jpg`

| | |
|---|---|
| sha256 | `2e74416cc81556c4a5f4c3ab36c50f9ad51d6b561706878e4ec91d22dc769ca1` |
| Bytes | 250,341 |
| Dimensions | 1391x807 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/939fc-rosa3.jpg |
| Capture | 2026-09-27T14:22:16+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `144_947a8-danielhaya6.jpg`

| | |
|---|---|
| sha256 | `cd6f31f33b9559c9a185f2fda7612019225ae9be3f1dfafd3fb294f3448d9d2e` |
| Bytes | 143,328 |
| Dimensions | 709x929 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/947a8-danielhaya6.jpg |
| Capture | 2026-09-27T14:22:17+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `145_949fa-fiqhhuman1.jpg`

| | |
|---|---|
| sha256 | `0071a5c98a8f278d7a205e8b66f4eea1e1c5788e9237ce06bd15bd759af63401` |
| Bytes | 240,846 |
| Dimensions | 766x891 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/949fa-fiqhhuman1.jpg |
| Capture | 2026-09-27T14:22:19+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `146_9555c-readinglist4.jpg`

| | |
|---|---|
| sha256 | `bf5e695c38a51b0366c8b6db402bea1d183f9953d52a0ebdd6ddf189fd8d42e5` |
| Bytes | 130,078 |
| Dimensions | 1332x635 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9555c-readinglist4.jpg |
| Capture | 2026-09-27T14:22:20+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `149_98077-errex7.jpg`

| | |
|---|---|
| sha256 | `12b81860e2255fe2ac9e89b83daab9e0d9cb3f02b3082ed803f15364626d0a1a` |
| Bytes | 155,098 |
| Dimensions | 909x575 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/98077-errex7.jpg |
| Capture | 2026-09-27T14:22:25+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `150_988c9-salvationcritic2.jpg`

| | |
|---|---|
| sha256 | `8186d326f426759edb69cf9af25a924f93d878463ed2d90883653e0f24616a58` |
| Bytes | 132,110 |
| Dimensions | 867x781 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/988c9-salvationcritic2.jpg |
| Capture | 2026-09-27T14:22:26+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `151_992c2-rosa2-e1596338718461.jpg`

| | |
|---|---|
| sha256 | `8f77bc2e9ea20c0a11c966afdf3b5a6f89a425a87ab938245661741505434601` |
| Bytes | 47,879 |
| Dimensions | 757x402 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/992c2-rosa2-e1596338718461.jpg |
| Capture | 2026-09-27T14:22:27+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `152_99396-jalajeltakfir.jpg`

| | |
|---|---|
| sha256 | `8e585e6cfe28d8cf539b7ba3c64fdbca72b571fed419521f165ef244955a08f1` |
| Bytes | 267,542 |
| Dimensions | 867x745 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/99396-jalajeltakfir.jpg |
| Capture | 2026-09-27T14:22:29+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `153_9b039-errex4.5.jpg`

| | |
|---|---|
| sha256 | `a81844d8ab153d483510277b1e51a77b853fa6455d55f8ab3c9184a4a6aaea33` |
| Bytes | 102,219 |
| Dimensions | 842x487 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9b039-errex4.5.jpg |
| Capture | 2026-09-27T14:22:30+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `155_9ca0f-errex2.jpg`

| | |
|---|---|
| sha256 | `f0ee528ffb97a21256e440a84acaacf518b859d0d311ca72d3e84e17e1d584d1` |
| Bytes | 180,359 |
| Dimensions | 835x685 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9ca0f-errex2.jpg |
| Capture | 2026-09-27T14:22:34+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `156_9cfa3-danielhijabi.jpg`

| | |
|---|---|
| sha256 | `b877531f3514661888e19931aac0ee221a0066d5ea7c019f70e0f106eb5ad710` |
| Bytes | 241,913 |
| Dimensions | 863x887 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9cfa3-danielhijabi.jpg |
| Capture | 2026-09-27T14:22:35+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of a Facebook post by Daniel Haqiqatjou on 'glamor hijabis' and glamour photos. |
| Alt text basis | written after viewing the image |

### `157_9d5e8-beat1.5.jpg`

| | |
|---|---|
| sha256 | `b0893086cd73c4dbb0cd04be3b86e96937f29a82d5b55f461e0f68ec42141ac1` |
| Bytes | 292,790 |
| Dimensions | 868x849 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9d5e8-beat1.5.jpg |
| Capture | 2026-09-27T14:22:37+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `159_9f6a7-unseen3.jpg`

| | |
|---|---|
| sha256 | `38f849b852c83dfa9f8177b9c616615aff36aa183af09a889423fa270d5e0e36` |
| Bytes | 34,989 |
| Dimensions | 1193x189 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9f6a7-unseen3.jpg |
| Capture | 2026-09-27T14:22:39+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `161_9fd10-slack3.jpg`

| | |
|---|---|
| sha256 | `66063923b5282e2e9652936c204bd2769cb74e017198ee2569abb60b95a3d5f8` |
| Bytes | 342,553 |
| Dimensions | 962x1600 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/9fd10-slack3.jpg |
| Capture | 2026-09-27T14:22:42+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `162_a0ea7-counter5.5.jpg`

| | |
|---|---|
| sha256 | `705c4b1a1f4c3777343747cf55a46ae9636c234ff8d499d40056457dc37033d9` |
| Bytes | 102,459 |
| Dimensions | 959x519 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a0ea7-counter5.5.jpg |
| Capture | 2026-09-27T14:22:43+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `164_a2fcb-slavery3.jpg`

| | |
|---|---|
| sha256 | `e153d4c4d268536544b69c8890d5bee5801ba576b6ee83ab324ee4309b6c0776` |
| Bytes | 275,086 |
| Dimensions | 1138x686 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a2fcb-slavery3.jpg |
| Capture | 2026-09-27T14:22:46+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `165_a625c-danielhaya17.jpg`

| | |
|---|---|
| sha256 | `be91376632a0ea7041910b7791e2b5e14db9c83b47f534c5aed3ca67e8fe2d3a` |
| Bytes | 113,039 |
| Dimensions | 749x762 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a625c-danielhaya17.jpg |
| Capture | 2026-09-27T14:22:47+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `166_a6680-fallacyex.jpg`

| | |
|---|---|
| sha256 | `2d9fc64ea758f1152443f2965cfe28990236d472c73f91cb6e280e85af4751e7` |
| Bytes | 68,251 |
| Dimensions | 774x238 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a6680-fallacyex.jpg |
| Capture | 2026-09-27T14:22:49+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `167_a668a-evo3.jpg`

| | |
|---|---|
| sha256 | `98203726e97e70742dda29f0a8ccc58f9fe7fe68929fd77304fea22df30865a0` |
| Bytes | 156,179 |
| Dimensions | 1140x460 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a668a-evo3.jpg |
| Capture | 2026-09-27T14:22:50+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `169_a8799-beat8.jpg`

| | |
|---|---|
| sha256 | `b151da78c8820ce8a250ef3ee3f06cb1bc77a5cd84e9d9a8d96beb87dd31738c` |
| Bytes | 248,501 |
| Dimensions | 795x908 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a8799-beat8.jpg |
| Capture | 2026-09-27T14:22:53+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `171_a96f0-dalia4.jpg`

| | |
|---|---|
| sha256 | `d8916e75359ee84aedf938e242524e653b61ababff9b992b8ed1976a515f677f` |
| Bytes | 91,964 |
| Dimensions | 971x338 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a96f0-dalia4.jpg |
| Capture | 2026-09-27T14:22:55+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `173_aa0bd-jazztweet.jpg`

| | |
|---|---|
| sha256 | `cb20cf4e30304e4177b89023d24603fed35f6d6718189cce7d69429451ef8909` |
| Bytes | 116,216 |
| Dimensions | 691x521 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/aa0bd-jazztweet.jpg |
| Capture | 2026-09-27T14:22:58+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `175_aba3c-symbol1.5.jpg`

| | |
|---|---|
| sha256 | `698f9aed0fccd4df38df162154c0dafe236a666d554bb1e9201ae612f216742b` |
| Bytes | 68,231 |
| Dimensions | 802x418 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/aba3c-symbol1.5.jpg |
| Capture | 2026-09-27T14:23:01+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `176_acd53-fiqhhuman2.1.jpg`

| | |
|---|---|
| sha256 | `e6641b1cad897dcfdb32b86be636ce9bc094b421bd0454ba9c17b03e10b9aefb` |
| Bytes | 176,702 |
| Dimensions | 666x629 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/acd53-fiqhhuman2.1.jpg |
| Capture | 2026-09-27T14:23:02+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `178_ad71b-symbol8.jpg`

| | |
|---|---|
| sha256 | `aa3a2a02b7b926c7a49f9e8192b7dc57a202cd375a254d07e65657d4451ec70c` |
| Bytes | 135,866 |
| Dimensions | 794x437 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ad71b-symbol8.jpg |
| Capture | 2026-09-27T14:23:05+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `181_af740-symbol3.jpg`

| | |
|---|---|
| sha256 | `72972ffe03b42e014de64b4619daca5cc38bc211e26c4ffab6b44dbd3c330913` |
| Bytes | 44,796 |
| Dimensions | 741x269 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/af740-symbol3.jpg |
| Capture | 2026-09-27T14:23:10+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `182_b2348-hijab6-1.jpg`

| | |
|---|---|
| sha256 | `c6904aaaee2ec61dc04872d901b5fcbb577641457326a2d4b98cf49d526f7028` |
| Bytes | 105,448 |
| Dimensions | 673x651 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/b2348-hijab6-1.jpg |
| Capture | 2026-09-27T14:23:11+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `186_b72f1-arnold1.jpg`

| | |
|---|---|
| sha256 | `68129f03c83a0f39fffd401123243c577b108d4d1f79516f3472dafd0d88d5e5` |
| Bytes | 227,230 |
| Dimensions | 918x837 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/b72f1-arnold1.jpg |
| Capture | 2026-09-27T14:23:17+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of a Yaqeen Institute article by Arnold Yasin Mol listing his papers on human rights in Islam. |
| Alt text basis | written after viewing the image |

### `187_b738f-beat7.jpg`

| | |
|---|---|
| sha256 | `babd44116cbafccadc21f988ff11c0f24103a028a27adf5170cc03a5a715e96c` |
| Bytes | 141,278 |
| Dimensions | 750x524 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/b738f-beat7.jpg |
| Capture | 2026-09-27T14:23:18+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `190_ba20e-jalajelcreds.jpg`

| | |
|---|---|
| sha256 | `3fe8b6abbd4a678dc36beaf6e960b84ff9fe4b79a152ec4d18c3bb03df4603f8` |
| Bytes | 116,563 |
| Dimensions | 520x934 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ba20e-jalajelcreds.jpg |
| Capture | 2026-09-27T14:23:23+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `191_baee9-fiqhhuman7.jpg`

| | |
|---|---|
| sha256 | `6ccb0d67f4de78f6e432172877b0da30591613aca0805cbf8f930572345e242a` |
| Bytes | 172,230 |
| Dimensions | 745x496 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/baee9-fiqhhuman7.jpg |
| Capture | 2026-09-27T14:23:24+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `192_bb488-symbol7.jpg`

| | |
|---|---|
| sha256 | `4831084ed60158a11c694a6d2532a157eb737749deeb9bd6630b81bd9d5b0e38` |
| Bytes | 166,881 |
| Dimensions | 775x544 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/bb488-symbol7.jpg |
| Capture | 2026-09-27T14:23:25+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `193_befd9-symbol11.jpg`

| | |
|---|---|
| sha256 | `b8344a768bcd906612a5e20045b226899891a61320df7580f1b23425820c3fbc` |
| Bytes | 107,779 |
| Dimensions | 794x433 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/befd9-symbol11.jpg |
| Capture | 2026-09-27T14:23:27+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `195_c1a56-8.jpg`

| | |
|---|---|
| sha256 | `1eaf980d7f7aaa37300a72c84451ec0bfd1299458300b97fe11ed8bd4229c3f9` |
| Bytes | 61,935 |
| Dimensions | 786x287 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c1a56-8.jpg |
| Capture | 2026-09-27T14:23:29+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `196_c2830-danieledits.jpg`

| | |
|---|---|
| sha256 | `a0135778fee115615177f28feeb48fa5f4841293fe1a021298f96522f041c5bb` |
| Bytes | 142,078 |
| Dimensions | 649x764 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c2830-danieledits.jpg |
| Capture | 2026-09-27T14:23:32+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `197_c384c-freedomempty.jpg`

| | |
|---|---|
| sha256 | `7b230a3b3e235573f54b614312d29d1950ec5705af1d58fd461fc5ad62ea5865` |
| Bytes | 102,083 |
| Dimensions | 735x282 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c384c-freedomempty.jpg |
| Capture | 2026-09-27T14:23:33+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `198_c58ad-beatpedant.jpg`

| | |
|---|---|
| sha256 | `25151246565260b056224f8cd0af8510b166a02004a94d72c26c6dec65e605f7` |
| Bytes | 181,073 |
| Dimensions | 773x922 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c58ad-beatpedant.jpg |
| Capture | 2026-09-27T14:23:35+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `199_c5c01-calculating.jpg`

| | |
|---|---|
| sha256 | `229a8eb3899666fed24c1300269a15ecdccd8d3df344a2132cc0f8c70f2e7d89` |
| Bytes | 141,140 |
| Dimensions | 1269x716 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c5c01-calculating.jpg |
| Capture | 2026-09-27T14:23:37+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `200_c6520-yes.jpg`

| | |
|---|---|
| sha256 | `ac4e2616039b62575ab30b3282f7bc14b07a4eb9604ad36aaf2bab09529b3fc1` |
| Bytes | 169,340 |
| Dimensions | 1322x870 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c6520-yes.jpg |
| Capture | 2026-09-27T14:23:39+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `201_c656e-convo3.jpg`

| | |
|---|---|
| sha256 | `270dde0cae73d4096461b7bb44ebb10176df57e91df7a98ab388546dc89f9da9` |
| Bytes | 242,784 |
| Dimensions | 1268x765 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c656e-convo3.jpg |
| Capture | 2026-09-27T14:23:40+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `202_c670b-arnoldbio.jpg`

| | |
|---|---|
| sha256 | `4cededca6da12458903219a9fb8e18b595f521748f70ad81d7e0f87effb7130a` |
| Bytes | 107,158 |
| Dimensions | 393x837 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c670b-arnoldbio.jpg |
| Capture | 2026-09-27T14:23:42+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `203_c6ba5-salvation4.jpg`

| | |
|---|---|
| sha256 | `a08eade01b258ac789bf53dccef147eae72fd25a9de3097b4938abbe05d7a191` |
| Bytes | 104,891 |
| Dimensions | 922x445 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c6ba5-salvation4.jpg |
| Capture | 2026-09-27T14:23:43+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `205_c8591-salvation5.6.jpg`

| | |
|---|---|
| sha256 | `e694ac93d6a80fdb432ebdf63019bd71bb8e393409cb1bc11869fd9af00d70e4` |
| Bytes | 159,040 |
| Dimensions | 847x474 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c8591-salvation5.6.jpg |
| Capture | 2026-09-27T14:23:46+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `206_c8965-symbolicex2.jpg`

| | |
|---|---|
| sha256 | `b8602066e628d75fead140e66cca2ed7e323b9538d75110cf152292794a85920` |
| Bytes | 79,642 |
| Dimensions | 812x245 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/c8965-symbolicex2.jpg |
| Capture | 2026-09-27T14:23:47+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `207_ca683-dalia8.jpg`

| | |
|---|---|
| sha256 | `29bd9bfd39f649cb61f0eacdef8a633f9642c2a2fae942a55b84bfd8c27c8107` |
| Bytes | 144,447 |
| Dimensions | 944x799 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ca683-dalia8.jpg |
| Capture | 2026-09-27T14:23:49+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `208_cc178-5.png`

| | |
|---|---|
| sha256 | `142183659e1b16b445fcc88adc71a2e5dc9790aa0c3be290b8855a02779c1b1f` |
| Bytes | 19,077 |
| Dimensions | 746x398 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/cc178-5.png |
| Capture | 2026-09-27T14:23:50+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `210_cc3a2-hijab8-1.jpg`

| | |
|---|---|
| sha256 | `643268bfaafa412b9c2a60b597d26fdde7489874b9ed0dfbf1708b1e1e14aab9` |
| Bytes | 94,419 |
| Dimensions | 688x660 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/cc3a2-hijab8-1.jpg |
| Capture | 2026-09-27T14:23:52+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `212_cddb8-danielhaya22.jpg`

| | |
|---|---|
| sha256 | `66a1457eba0d9563bc7412403ff1b2a697b37a877c9a8fbc48df4e13d5417535` |
| Bytes | 133,577 |
| Dimensions | 632x867 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/cddb8-danielhaya22.jpg |
| Capture | 2026-09-27T14:23:56+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `213_cf900-beat6.2.jpg`

| | |
|---|---|
| sha256 | `17ad3ec93c9b59ebb09dc1d72ab089d409d43a7a3576179e93f48f8bb98606a4` |
| Bytes | 86,660 |
| Dimensions | 773x343 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/cf900-beat6.2.jpg |
| Capture | 2026-09-27T14:23:57+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `214_cfb37-intolerancereligious.jpg`

| | |
|---|---|
| sha256 | `064a0484745d0f0bd9ae4329671a518f5d42dffe0b47ce03d990fe444ac9d635` |
| Bytes | 112,915 |
| Dimensions | 989x521 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/cfb37-intolerancereligious.jpg |
| Capture | 2026-09-27T14:23:59+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `215_cfe63-beat2.jpg`

| | |
|---|---|
| sha256 | `4ca9f60a0ea3b2e1a8e311aff5532d6395df961eb0fc547a75da68d78ebc53f4` |
| Bytes | 74,381 |
| Dimensions | 766x296 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/cfe63-beat2.jpg |
| Capture | 2026-09-27T14:24:00+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `216_d144d-8.6.jpg`

| | |
|---|---|
| sha256 | `59c736ae315cbbfe81d9a3c39e3c28a25b5c1334a6bcac7e8a9b7fe9153a29ab` |
| Bytes | 143,437 |
| Dimensions | 775x440 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/d144d-8.6.jpg |
| Capture | 2026-09-27T14:24:02+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `218_d2e3b-dalia1.jpg`

| | |
|---|---|
| sha256 | `05cb913a877ac909cd44b9a3a84de155064d03e531a44120d2515b81415b553d` |
| Bytes | 174,019 |
| Dimensions | 989x752 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/d2e3b-dalia1.jpg |
| Capture | 2026-09-27T14:24:04+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `219_d410a-danielresponseevo1.jpg`

| | |
|---|---|
| sha256 | `087ea8badbf0c4fcaf106ed75702ebd1198ac399d6921e10bf6f180212c5213c` |
| Bytes | 145,252 |
| Dimensions | 1154x402 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/d410a-danielresponseevo1.jpg |
| Capture | 2026-09-27T14:24:06+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `220_d4883-3.png`

| | |
|---|---|
| sha256 | `7418424fb4e36156076b35211c923396bd0093b50ceae090e0c669d4ffea7284` |
| Bytes | 46,862 |
| Dimensions | 809x759 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/d4883-3.png |
| Capture | 2026-09-27T14:24:07+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `223_d7807-salvation9.jpg`

| | |
|---|---|
| sha256 | `aa2709aadc64d6de13b3a3b089bb2ec4a7e666b65ccbd7f7ec0d496174012302` |
| Bytes | 230,191 |
| Dimensions | 864x753 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/d7807-salvation9.jpg |
| Capture | 2026-09-27T14:24:11+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `224_d8804-foucault2.jpg`

| | |
|---|---|
| sha256 | `5e200c888d72c66cc4a78399b816bba303f334e21b3ff1169208dbc0cff4b6a0` |
| Bytes | 140,770 |
| Dimensions | 811x833 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/d8804-foucault2.jpg |
| Capture | 2026-09-27T14:24:12+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `228_e39aa-salvation2.jpg`

| | |
|---|---|
| sha256 | `0a74d176b8c037a692d05ccaafe65bae347fa9c03df8ecc74d7b65c2fe1e1581` |
| Bytes | 109,450 |
| Dimensions | 982x403 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/e39aa-salvation2.jpg |
| Capture | 2026-09-27T14:24:19+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `229_e614e-musa2.jpg`

| | |
|---|---|
| sha256 | `d3648477a50fb3214254338bddc5604cea6237a582fa3fabd250b53daf2d116a` |
| Bytes | 72,824 |
| Dimensions | 818x308 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/e614e-musa2.jpg |
| Capture | 2026-09-27T14:24:20+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `230_e7b8e-symbol6.jpg`

| | |
|---|---|
| sha256 | `f4046700bdfbecd9b4622fd8e4c9e60832e1820f0ee858e1b246b50471a67cc4` |
| Bytes | 97,046 |
| Dimensions | 767x375 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/e7b8e-symbol6.jpg |
| Capture | 2026-09-27T14:24:21+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `231_e8350-evo8.jpg`

| | |
|---|---|
| sha256 | `49fa341a6c63d5e10a5f47456270b68fe737c61c46a375b77242308eed034ac6` |
| Bytes | 217,780 |
| Dimensions | 1120x849 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/e8350-evo8.jpg |
| Capture | 2026-09-27T14:24:22+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `232_e9ebf-dalia5.jpg`

| | |
|---|---|
| sha256 | `d3be7e5c688f2b233ac3e8490e99145afdd622dde4440bb8979ea4577b3befaa` |
| Bytes | 170,284 |
| Dimensions | 971x553 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/e9ebf-dalia5.jpg |
| Capture | 2026-09-27T14:24:24+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `234_ecaec-4.png`

| | |
|---|---|
| sha256 | `aa0a55cbfea8a58a1b402b33c8fe517354162c7719bc651d2125503b65d1032f` |
| Bytes | 19,964 |
| Dimensions | 711x279 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ecaec-4.png |
| Capture | 2026-09-27T14:24:27+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `235_ed124-fiqhhuman4.jpg`

| | |
|---|---|
| sha256 | `f0dbaf2e83f0ff2deadf7031bb14856a0a69d4d4aea3cc01ee36070a12a0065a` |
| Bytes | 325,190 |
| Dimensions | 744x1016 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ed124-fiqhhuman4.jpg |
| Capture | 2026-09-27T14:24:28+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `236_ed1ea-jalajelview.jpg`

| | |
|---|---|
| sha256 | `01165c7f84b30e80a7aa946eca383084a30572a69e8f6d2ae779ad7f91a57236` |
| Bytes | 82,662 |
| Dimensions | 842x310 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ed1ea-jalajelview.jpg |
| Capture | 2026-09-27T14:24:30+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `237_edd28-symbol5.jpg`

| | |
|---|---|
| sha256 | `003bb058267d13f4d441c52c54eba92567f2eefc0b3e820585944a93440ef960` |
| Bytes | 156,600 |
| Dimensions | 754x559 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/edd28-symbol5.jpg |
| Capture | 2026-09-27T14:24:31+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `238_ee9b7-clause2.jpg`

| | |
|---|---|
| sha256 | `bf1d7e0f2df3b2a67cfac8e4113532ec41db366940e0e8574fdfbe00c4aa02e3` |
| Bytes | 74,219 |
| Dimensions | 804x281 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ee9b7-clause2.jpg |
| Capture | 2026-09-27T14:24:32+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `240_efdc1-salvation7.jpg`

| | |
|---|---|
| sha256 | `55190291cc1791a70ff7eff0a164a265b0891713b90656cefcd1b5ed87a62988` |
| Bytes | 145,793 |
| Dimensions | 864x611 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/efdc1-salvation7.jpg |
| Capture | 2026-09-27T14:24:35+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `243_f32fd-salvation4.5.jpg`

| | |
|---|---|
| sha256 | `ef6231d071c1eacc01a0d673bceec152328d46ceca760d81e0ada9c5e4fea5c7` |
| Bytes | 174,401 |
| Dimensions | 864x587 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/f32fd-salvation4.5.jpg |
| Capture | 2026-09-27T14:24:39+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `244_f562f-foucault.jpg`

| | |
|---|---|
| sha256 | `31e9fee68b0d4db26bf6c199bdf99d7f9a0333116460ac3ec737a610a163cd56` |
| Bytes | 169,817 |
| Dimensions | 775x605 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/f562f-foucault.jpg |
| Capture | 2026-09-27T14:24:40+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `245_f8f98-counter4.jpg`

| | |
|---|---|
| sha256 | `b02ccb85c43866e9ed7cf66555ca8250b13a9c728550f063f6be8474ef73d72a` |
| Bytes | 321,332 |
| Dimensions | 972x907 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/f8f98-counter4.jpg |
| Capture | 2026-09-27T14:24:41+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `247_fa898-10.jpg`

| | |
|---|---|
| sha256 | `055cd242209f966fc97a752224d45b2057746a033663904e8e9734c893ecec53` |
| Bytes | 132,733 |
| Dimensions | 766x528 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/fa898-10.jpg |
| Capture | 2026-09-27T14:24:45+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `248_fbf15-hr2.jpg`

| | |
|---|---|
| sha256 | `390ff8d65c84a31840a72fb710bc6ad5d31d6790213dad2356fcd3b4c40b3015` |
| Bytes | 191,812 |
| Dimensions | 880x722 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/fbf15-hr2.jpg |
| Capture | 2026-09-27T14:24:46+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `249_fc1e2-evo4.jpg`

| | |
|---|---|
| sha256 | `487cf9002de362b4ae8fb48d3cbe10ef55d25bbb6de33559ad144bad7b53f34e` |
| Bytes | 207,017 |
| Dimensions | 1140x819 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/fc1e2-evo4.jpg |
| Capture | 2026-09-27T14:24:48+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `251_fd8b8-daliafb.jpg`

| | |
|---|---|
| sha256 | `38b659ee76ce6ec9c58067f1319e5c88f5a273a0fd59490a3babf7b1f4aaf77e` |
| Bytes | 200,885 |
| Dimensions | 800x721 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/fd8b8-daliafb.jpg |
| Capture | 2026-09-27T14:24:50+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `253_feb8f-beat6.1.jpg`

| | |
|---|---|
| sha256 | `a5e9dfb093044934ce8e391f31f840e8da0c806148a5e68bd7adff89044f0795` |
| Bytes | 54,743 |
| Dimensions | 773x288 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/feb8f-beat6.1.jpg |
| Capture | 2026-09-27T14:24:53+05:30 |
| Role in the post | `img:src` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `256_ff1e4-eq4.5.jpg`

| | |
|---|---|
| sha256 | `75f38d575b0e8b64c6d12371f95b3bf7bc78281bac7f1f45be5cf431244ec9c4` |
| Bytes | 22,642 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ff1e4-eq4.5.jpg |
| Capture | 2026-09-27T14:24:57+05:30 |
| Role in the post | `img:src+img:srcset` |
| Work | `reviewing-haqiqatjou` (The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `259_225a3-e2.jpg`

| | |
|---|---|
| sha256 | `be2b176bb853bd81b800fad1be98130ed78244e271f6c8c8eac6ddd0e3e07e6f` |
| Bytes | 19,945 |
| Dimensions | 873x110 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/225a3-e2.jpg |
| Capture | 2026-09-27T14:25:04+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `260_4421c-e6.5.jpg`

| | |
|---|---|
| sha256 | `2fdd82440864c9de39a1b84be718f1478b9d613119377a2fb80a52854cfda457` |
| Bytes | 269,262 |
| Dimensions | 747x859 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4421c-e6.5.jpg |
| Capture | 2026-09-27T14:25:06+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `261_4d858-e7.jpg`

| | |
|---|---|
| sha256 | `6d5d2d283622686b8a6f092579d61806bc38791746fb422e32665ad54b3f1801` |
| Bytes | 95,265 |
| Dimensions | 718x467 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/4d858-e7.jpg |
| Capture | 2026-09-27T14:25:07+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `262_5e90c-davidpic.jpg`

| | |
|---|---|
| sha256 | `9bb12226981621869ccfd500a41085d56879fc40a6e8773b83f0ba435e2e4564` |
| Bytes | 121,622 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/5e90c-davidpic.jpg |
| Capture | 2026-09-27T14:25:08+05:30 |
| Role in the post | `featured_media` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Dr David Jalajel, author of “Adam is No Myth”, speaking at a conference while wearing a UNFCCC lanyard. |
| Alt text basis | written after viewing the image |

### `263_a56b2-e5.jpg`

| | |
|---|---|
| sha256 | `bd6e2f4e376f88e5cb77d41695cfdb0e45d0c61e86f26570853caff30a216fac` |
| Bytes | 147,882 |
| Dimensions | 873x551 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/a56b2-e5.jpg |
| Capture | 2026-09-27T14:25:09+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `264_ab89e-e3.jpg`

| | |
|---|---|
| sha256 | `5e87c4d4281295afbef143f950a803f6de6f518697a893dd4055eed139596353` |
| Bytes | 54,030 |
| Dimensions | 873x235 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/ab89e-e3.jpg |
| Capture | 2026-09-27T14:25:10+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `265_b0fd7-e1.jpg`

| | |
|---|---|
| sha256 | `187988db0926fa094f2192b4a000721c9bb0850d5dad701ed6d55c6c28f052bb` |
| Bytes | 77,519 |
| Dimensions | 873x304 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/b0fd7-e1.jpg |
| Capture | 2026-09-27T14:25:12+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `266_eafe1-e4.jpg`

| | |
|---|---|
| sha256 | `eb5d010aae5084cdb42617f2c8636f23cca30717b0a0b6724cf88b35c632b4a5` |
| Bytes | 32,825 |
| Dimensions | 873x169 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2022/05/eafe1-e4.jpg |
| Capture | 2026-09-27T14:25:13+05:30 |
| Role in the post | `img:src` |
| Work | `adam-is-no-myth` (Adam Is No “Myth”) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Adam Is No “Myth”' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `267_comiccover1.png`

| | |
|---|---|
| sha256 | `044686af1029fa4000a9c2e9fbb03ed9a428de644bcbb63eb564e45f9cf3da01` |
| Bytes | 324,450 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/comiccover1.png |
| Capture | 2026-09-27T14:25:14+05:30 |
| Role in the post | `featured_media` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `268_slide1.png`

| | |
|---|---|
| sha256 | `2b4abcd8949dbbf68ef8417c61c3a1f4125012b06005a970cea015f3707641a6` |
| Bytes | 91,364 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide1.png |
| Capture | 2026-09-27T14:25:17+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `269_slide10.png`

| | |
|---|---|
| sha256 | `bcfffa2168d489e4ef1c8011bb153ae821e3429cdcd8c084a05db0d8bc24e7b0` |
| Bytes | 1,051,820 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide10.png |
| Capture | 2026-09-27T14:25:18+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Comic plate: an illustrated book-lined stone room captioned 'Welcome to the Islam Directory program.' |
| Alt text basis | written after viewing the image |

### `270_slide11.png`

| | |
|---|---|
| sha256 | `94ac96408c1049ef8c0f63c8a04c99d6e8322c0b5b15748eae6615fbc5bffa38` |
| Bytes | 741,126 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide11.png |
| Capture | 2026-09-27T14:25:20+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `271_slide12.png`

| | |
|---|---|
| sha256 | `2df5a1ffb004baba5400f218f92445085273ecabbcc9b338ac3afb111e9141ef` |
| Bytes | 890,916 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide12.png |
| Capture | 2026-09-27T14:25:22+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `272_slide13.png`

| | |
|---|---|
| sha256 | `e4749a26569e46f5e5d7f2d2fb543798ba2477e9ba255914039f8b69a6357299` |
| Bytes | 508,907 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide13.png |
| Capture | 2026-09-27T14:25:24+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `273_slide14.png`

| | |
|---|---|
| sha256 | `476cf8ae549277f3c1f3fba7b89528c45f03e24c86227c99ee6aa033f5f35a82` |
| Bytes | 1,014,977 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide14.png |
| Capture | 2026-09-27T14:25:26+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `274_slide15.png`

| | |
|---|---|
| sha256 | `2b4ce6e8351932268134f54939f541cca97dcd186a47739a5fdee473bf204964` |
| Bytes | 875,959 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide15.png |
| Capture | 2026-09-27T14:25:28+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `275_slide16.png`

| | |
|---|---|
| sha256 | `727d0811d5e252203462a7c907eafac066d9920687d2554d7b624aa467ee0cd9` |
| Bytes | 797,313 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide16.png |
| Capture | 2026-09-27T14:25:30+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `276_slide17.png`

| | |
|---|---|
| sha256 | `b2b1fc6c4ddb46cdd8e47aa126b42f3f168163064fc398ee21341b7438e3e0fc` |
| Bytes | 911,553 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide17.png |
| Capture | 2026-09-27T14:25:32+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `277_slide18.png`

| | |
|---|---|
| sha256 | `fd0336433142a555d7a130d2aede2d9ea80a5a6a16193382117c73aa0a7c31fc` |
| Bytes | 363,855 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide18.png |
| Capture | 2026-09-27T14:25:34+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `278_slide19.png`

| | |
|---|---|
| sha256 | `b6305cbd5715575b10fbf16500abdba24ebe0456730359711782f363b0ce7416` |
| Bytes | 520,699 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide19.png |
| Capture | 2026-09-27T14:25:35+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `279_slide2.png`

| | |
|---|---|
| sha256 | `f8bd7e67f03b607cc4c34fab54d81b3631a254fe1bb1070eb8abbfb3cdd9a1d1` |
| Bytes | 534,011 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide2.png |
| Capture | 2026-09-27T14:25:37+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `280_slide20.png`

| | |
|---|---|
| sha256 | `7407bb573fa122ec6e845d338b940f714b2a5377448c3f63b35e321e168fd5e9` |
| Bytes | 1,026,422 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide20.png |
| Capture | 2026-09-27T14:25:38+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Comic plate: the same illustrated room captioned 'Do you have any additional queries?' and 'No? I see. Then allow me to return you to the lobby.' |
| Alt text basis | written after viewing the image |

### `281_slide21.png`

| | |
|---|---|
| sha256 | `88b7e74a39aadbafea74226febd34262f93583cb46b366b2cc1bb097105db531` |
| Bytes | 472,601 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide21.png |
| Capture | 2026-09-27T14:25:40+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `282_slide22.png`

| | |
|---|---|
| sha256 | `ec7d4a406287f1577f33472603401020e00240dda713ff8c93ea97e35c7e6dec` |
| Bytes | 359,817 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide22.png |
| Capture | 2026-09-27T14:25:41+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `283_slide3.png`

| | |
|---|---|
| sha256 | `c31ddd917b74a5910582ac318d4f31c4c23ab6fc3b3ac27361b49db76cd2957f` |
| Bytes | 341,878 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide3.png |
| Capture | 2026-09-27T14:25:43+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `284_slide4.png`

| | |
|---|---|
| sha256 | `7380ff05bec5b79f1c942d77b37352d9922f8ecf37ec8fb98737c997e2aad6eb` |
| Bytes | 540,269 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide4.png |
| Capture | 2026-09-27T14:25:45+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `285_slide5.png`

| | |
|---|---|
| sha256 | `70fda7dcfe48b10c8246f100b57d422df5a22efbf14ab5f566376d0d259bff96` |
| Bytes | 619,009 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide5.png |
| Capture | 2026-09-27T14:25:47+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `286_slide6.png`

| | |
|---|---|
| sha256 | `e1a079cc998e38db31391f744f36daeea6868b0ab133be51e7955b1242f4ad6e` |
| Bytes | 629,096 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide6.png |
| Capture | 2026-09-27T14:25:48+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `287_slide7.png`

| | |
|---|---|
| sha256 | `2bab9e4042b23a47feaad1a4b986e53c7c99f238fd177d46a12eeb9a8141d6ed` |
| Bytes | 404,972 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide7.png |
| Capture | 2026-09-27T14:25:50+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `288_slide8.png`

| | |
|---|---|
| sha256 | `55f0e265236af4c3f47a80d461c89b8ea6f80e7fd1aff58ba919f61685fde99b` |
| Bytes | 477,316 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide8.png |
| Capture | 2026-09-27T14:25:52+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `289_slide9.png`

| | |
|---|---|
| sha256 | `f53cbd5cb4b0ea48954fe0b1f147898f275a445e29b4ad10495922c8591926a7` |
| Bytes | 617,080 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/slide9.png |
| Capture | 2026-09-27T14:25:55+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `ijihad-1` (iJihad 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iJihad 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `290_time-travel_resize_md.jpg`

| | |
|---|---|
| sha256 | `a0cda083d3ae3ae3ba5ba07292f09899e32fdcf70df69e3036a87298c7ba6598` |
| Bytes | 125,961 |
| Dimensions | 744x389 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/03/time-travel_resize_md.jpg |
| Capture | 2026-09-27T14:25:56+05:30 |
| Role in the post | `featured_media` |
| Work | `lost-in-time-translation` (Lost in Time-Translation) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A science-fiction illustration of a man seen from behind, chained to a heavy ball, facing a glowing blue portal in a ruined industrial interior. |
| Alt text basis | written after viewing the image |

### `291_anatomical_theatre_leiden-e1579806797851.jpg`

| | |
|---|---|
| sha256 | `3040422456abf85b050ad6deb92539dfd0798d96fc62da393f0d935b29cc43aa` |
| Bytes | 1,023,431 |
| Dimensions | 2131x1014 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/01/anatomical_theatre_leiden-e1579806797851.jpg |
| Capture | 2026-09-27T14:25:58+05:30 |
| Role in the post | `featured_media` |
| Work | `backbone-ribs` (Between a Backbone and Ribs: How Science Obscures the Beauty of the Qur’an) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A seventeenth-century engraving of the Anatomical Theatre at Leiden, an oval dissecting arena ringed by tiered galleries of onlookers and skeletons. |
| Alt text basis | written after viewing the image |

### `292_humanorigingraph.png`

| | |
|---|---|
| sha256 | `9cc5472111844151670ba02eade0863f51549897d0d9e43fa0032f9ae2b39604` |
| Bytes | 165,031 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/01/humanorigingraph.png |
| Capture | 2026-09-27T14:25:59+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src` |
| Work | `backbone-ribs` (Between a Backbone and Ribs: How Science Obscures the Beauty of the Qur’an) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Between a Backbone and Ribs: How Science Obscures the Beauty of the Qur’an' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `293_taraib.png`

| | |
|---|---|
| sha256 | `f8d41c213cb30f0de1fc788aa87ffd9ee359e88fd56426cec99e59045ef9544d` |
| Bytes | 209,730 |
| Dimensions | 899x441 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2020/01/taraib.png |
| Capture | 2026-09-27T14:26:01+05:30 |
| Role in the post | `img:data-large-file+img:data-orig-file+img:src` |
| Work | `backbone-ribs` (Between a Backbone and Ribs: How Science Obscures the Beauty of the Qur’an) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Between a Backbone and Ribs: How Science Obscures the Beauty of the Qur’an' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `294_cover.png`

| | |
|---|---|
| sha256 | `0be8852fa34c4b3a1e73cd8e78497280e257054c622aa80f3fa1260a3b337eed` |
| Bytes | 150,138 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/12/cover.png |
| Capture | 2026-09-27T14:26:03+05:30 |
| Role in the post | `featured_media` |
| Work | `ikhalifa-ep-2` (iKhalifa Ep. 2) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | The title graphic for episode 2 of the “i Khalifa” comic: the word “iKHALIFA” in blue above a ripple, over a large black numeral 2. |
| Alt text basis | written after viewing the image |

### `295_cover1.png`

| | |
|---|---|
| sha256 | `9537c67726297bfa759a7c3603ee16a4504840a176a7bc7cfd190f7121e6126d` |
| Bytes | 144,643 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/12/cover1.png |
| Capture | 2026-09-27T14:26:05+05:30 |
| Role in the post | `featured_media` |
| Work | `ikhalifa-ep-1` (iKhilafa (Episode 1)) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'iKhilafa (Episode 1)' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `296_islam-view-liberals.jpg`

| | |
|---|---|
| sha256 | `97ff57bb8267a06d2a6fe3e07ded750789cee48e8304a160259854638be74092` |
| Bytes | 45,706 |
| Dimensions | 717x440 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/11/islam-view-liberals.jpg |
| Capture | 2026-09-27T14:26:06+05:30 |
| Role in the post | `featured_media` |
| Work | `liberalism-in-the-muslim-world` (Liberalism in the Muslim World) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Liberalism in the Muslim World' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `297_hard-trivia-questions-3.jpg`

| | |
|---|---|
| sha256 | `67858624e64e961772e44eb3ba079819a30378d75096bfabe61d4ef91df65e30` |
| Bytes | 195,727 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/11/hard-trivia-questions-3.jpg |
| Capture | 2026-09-27T14:26:07+05:30 |
| Role in the post | `featured_media` |
| Work | `hard-questions-answering-doubts-about-islam` (Hard Questions: Answering Doubts About Islam) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A title card reading “Hard Questions”, with a large question mark drawn in overlapping blue outline strokes on black. |
| Alt text basis | written after viewing the image |

### `298_sciencepresentcover.png`

| | |
|---|---|
| sha256 | `719111f51be6950ee18df5bdd906085b9bc2c84da2bb8ad5eb63623eeb9db318` |
| Bytes | 1,470,051 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/11/sciencepresentcover.png |
| Capture | 2026-09-27T14:26:09+05:30 |
| Role in the post | `featured_media` |
| Work | `the-quran-science-a-forced-marriage` (The Quran, Science: A Forced Marriage) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Title graphic reading 'The Qur'an & Science: A Forced Marriage' over a photograph of a brass astrolabe. |
| Alt text basis | written after viewing the image |

### `299_aisha_s-age_1-heroimage-1500x500.jpg`

| | |
|---|---|
| sha256 | `65e33c95cfdaa133b09a9a7fa2106da3ca54c3094c5e0539247e94fb4e403aff` |
| Bytes | 64,642 |
| Dimensions | 1500x500 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/10/aisha_s-age_1-heroimage-1500x500.jpg |
| Capture | 2026-09-27T14:26:10+05:30 |
| Role in the post | `featured_media` |
| Work | `understanding-aishas-age-an-interdisciplinary-approach` (Understanding Aisha’s Age: An Interdisciplinary Approach) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A model of an earthen courtyard house with date palms and clay water jars, its flat-roofed walls pierced by small square openings. |
| Alt text basis | written after viewing the image |

### `300_shutterstock_434295161.jpg`

| | |
|---|---|
| sha256 | `cdc6f4618b52e094c6c7e68777de4fe0c25d62a581979e889e89ab6bc724ce42` |
| Bytes | 57,120 |
| Dimensions | 1000x750 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/08/shutterstock_434295161.jpg |
| Capture | 2026-09-27T14:26:11+05:30 |
| Role in the post | `featured_media` |
| Work | `yolo-a-motto-of-ignorance` (#YOLO: A Motto of Ignorance) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A stock 3D illustration of a seesaw with a crowned, smiling gold ball at one end and a frowning gold ball at the other. |
| Alt text basis | written after viewing the image |

### `301_justice.jpg`

| | |
|---|---|
| sha256 | `5aa7bea87de593df410a0539a25bd3cb9f978d9aa37f810840ca419023082b1b` |
| Bytes | 4,741,086 |
| Dimensions | 4256x2832 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/08/justice.jpg |
| Capture | 2026-09-27T14:26:15+05:30 |
| Role in the post | `featured_media` |
| Work | `gods-mercy-without-eternal-punishment` (The Fire of God’s Mercy) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A low-angle photograph of the Lady Justice statue, her sword lowered and her scales raised against a blue and clouded sky. |
| Alt text basis | written after viewing the image |

### `302_m102311.jpg`

| | |
|---|---|
| sha256 | `2265ebbb6caebe28ba8aa8beba1763f62da51a0a2f2bfcab358678ff8e502b2e` |
| Bytes | 40,153 |
| Dimensions | 685x400 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/06/m102311.jpg |
| Capture | 2026-09-27T14:26:16+05:30 |
| Role in the post | `featured_media` |
| Work | `an-alternate-reality` (An Alternate Reality) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A portrait of a seated man in Ottoman dress — a large yellow turban and an orange robe under a fur-trimmed cloak — against a plain brown backdrop. |
| Alt text basis | written after viewing the image |

### `303_b803d6cec0e6196249e90767af9949d4.jpg`

| | |
|---|---|
| sha256 | `99b047c26c02e342896bcc21c718aad547d1c7b564bc3b2bd82d56d1246fff51` |
| Bytes | 114,807 |
| Dimensions | 1600x1200 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/06/b803d6cec0e6196249e90767af9949d4.jpg |
| Capture | 2026-09-27T14:26:17+05:30 |
| Role in the post | `featured_media` |
| Work | `atheism-doubting-your-doubts` (Atheism: Doubting Your Doubts) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A computer render of a chessboard on which the black king has been toppled, its fallen cross-head lying beside it among the standing white pieces. |
| Alt text basis | written after viewing the image |

### `304_trumpnaked1.png`

| | |
|---|---|
| sha256 | `579561f4b6f093c2b6f9de1f825fc44612615cad48b29a0593f9f9e51dc5dda1` |
| Bytes | 708,253 |
| Dimensions | 760x568 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/05/trumpnaked1.png |
| Capture | 2026-09-27T14:26:19+05:30 |
| Role in the post | `featured_media` |
| Work | `naked-kings-in-the-information-age` (Naked Kings in the Information Age) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A political cartoon of Donald Trump as a naked emperor, his crown and sceptre removed and the figure censored, standing before a line of Republican elephants in suits. |
| Alt text basis | written after viewing the image |

### `305_madmal.png`

| | |
|---|---|
| sha256 | `89429b98d53ac2a8832e8ec587476c6f274f6b013103025325e024474cc0fcc9` |
| Bytes | 657,056 |
| Dimensions | 1280x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/05/madmal.png |
| Capture | 2026-09-27T14:26:21+05:30 |
| Role in the post | `featured_media` |
| Work | `islam-science-and-history` (Islam, Science, and History) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | The “Mad Mamluks” channel banner: the title in black on a yellow octagon beside a portrait of the channel's host. |
| Alt text basis | written after viewing the image |

### `306_news1856.jpg`

| | |
|---|---|
| sha256 | `4023ae183275fc440c28ee8fb702226aae0fa54122ad747eef7a9601b306e0e6` |
| Bytes | 97,400 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/03/news1856.jpg |
| Capture | 2026-09-27T14:26:22+05:30 |
| Role in the post | `featured_media` |
| Work | `when-religion-becomes-confusing` (When Religion Becomes Confusing) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'When Religion Becomes Confusing' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `307_annefrankjapan-1024x640.jpg`

| | |
|---|---|
| sha256 | `fb2e40ebadb9f5abcce59be2f0928031c103c26d7859fd0822d2b62647794736` |
| Bytes | 76,664 |
| Dimensions | 1024x640 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/03/annefrankjapan-1024x640.jpg |
| Capture | 2026-09-27T14:26:23+05:30 |
| Role in the post | `featured_media` |
| Work | `of-context-and-confusion` (Of Context and Confusion) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | An illustration of a schoolgirl holding books and a pen, standing before a red disc bearing a swastika — here the Nazi emblem, not the Hindu symbol. |
| Alt text basis | written after viewing the image |

### `308_26scifi-hughes.jpg`

| | |
|---|---|
| sha256 | `3fd4cc95a465352f5a6da6ec05625625b776b52f4864923bc07563e0c7833d7e` |
| Bytes | 46,792 |
| Dimensions | 900x531 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2018/03/26scifi-hughes.jpg |
| Capture | 2026-09-27T14:26:24+05:30 |
| Role in the post | `featured_media` |
| Work | `a-muslims-guide-to-science-scientism` (A Muslim's Guide to Science: Scientism) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'A Muslim's Guide to Science: Scientism' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `309_quran-2478729__480.jpg`

| | |
|---|---|
| sha256 | `f24ea7044a1eb012139c108b79d3a02c173af6e2acbd29a79238b7fbf663ca0c` |
| Bytes | 138,671 |
| Dimensions | 853x480 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/12/quran-2478729__480.jpg |
| Capture | 2026-09-27T14:26:26+05:30 |
| Role in the post | `featured_media` |
| Work | `the-atheistic-worldview-vs-the-quranic-worldview` (The Atheistic Worldview vs. The Qur’anic Worldview) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | An illuminated opening page of a Qur'an, the Arabic text of al-Fatiha set inside a floral and geometric border. |
| Alt text basis | written after viewing the image |

### `310_maxresdefault.jpg`

| | |
|---|---|
| sha256 | `9f49c787a919855c1f874467674813e560649fc9ea558c0c4b27fd1c256308a3` |
| Bytes | 116,720 |
| Dimensions | 2352x1322 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/12/maxresdefault.jpg |
| Capture | 2026-09-27T14:26:27+05:30 |
| Role in the post | `featured_media` |
| Work | `extremism-in-muslim-thought` (Extremism in Muslim Thought) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Extremism in Muslim Thought' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `311_revitalising-the-ecological-ethics-of-islam-by-way-of-islamic-education.jpg`

| | |
|---|---|
| sha256 | `5ed15840b679d91b25e2900f945adbb0d1771cd49d1781517dd4b353c19ad610` |
| Bytes | 135,164 |
| Dimensions | 1500x655 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/12/revitalising-the-ecological-ethics-of-islam-by-way-of-islamic-education.jpg |
| Capture | 2026-09-27T14:26:29+05:30 |
| Role in the post | `featured_media` |
| Work | `islam-and-litter-reduction` (Islam and Litter Reduction) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Islam and Litter Reduction' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `312_liberalism_type_clipped_rev_1-e1513921665445.png`

| | |
|---|---|
| sha256 | `424cbf68489dcc951dfdbc20797e611334b2ea30eda8c6c0713a6d5f68136f3b` |
| Bytes | 331,847 |
| Dimensions | 960x720 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/12/liberalism_type_clipped_rev_1-e1513921665445.png |
| Capture | 2026-09-27T14:26:30+05:30 |
| Role in the post | `featured_media` |
| Work | `liberalism-in-muslim-thought` (Liberalism in Muslim Thought) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Liberalism in Muslim Thought' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `313_160829-weiss-leaked-isis-docs-tease_g5fid0.jpg`

| | |
|---|---|
| sha256 | `7751ea65ba3112cbe3274883a35a2fbc50c3efe9d1876568fb3ebc8512b50fd6` |
| Bytes | 141,014 |
| Dimensions | 1480x832 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/12/160829-weiss-leaked-isis-docs-tease_g5fid0.jpg |
| Capture | 2026-09-27T14:26:32+05:30 |
| Role in the post | `featured_media` |
| Work | `islam-and-terrorism` (Islam and Terrorism) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Islam and Terrorism' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `314_540487_whswcsns.jpg`

| | |
|---|---|
| sha256 | `00d28135a2d46694ada58038f4662b92bbbebf4cea7c6f315c97b71a4d39725e` |
| Bytes | 53,417 |
| Dimensions | 600x450 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/12/540487_whswcsns.jpg |
| Capture | 2026-09-27T14:26:33+05:30 |
| Role in the post | `featured_media` |
| Work | `understanding-atheism` (Understanding Atheism) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A painting of four men huddled together, one holding a glass, their faces rendered in heavy, worried brushstrokes. |
| Alt text basis | written after viewing the image |

### `315_scienceislam.jpg`

| | |
|---|---|
| sha256 | `68e2f00dce916756ebbd9d416adc80493d40913af3ea1ee96268215bf90efd02` |
| Bytes | 111,437 |
| Dimensions | 640x480 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2017/05/scienceislam.jpg |
| Capture | 2026-09-27T14:26:35+05:30 |
| Role in the post | `featured_media` |
| Work | `the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables` (The Structure of Scientific Productivity in Islamic Civilization: Orientalists’ Fables) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Structure of Scientific Productivity in Islamic Civilization: Orientalists’ Fables' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `316_allah-calligraphy-yellow-wallpaper.jpg`

| | |
|---|---|
| sha256 | `44c0e6be7f1b941fe1f8bf4d72c8d0fdbe37d0ab9c436f170b0cf88dd7af069b` |
| Bytes | 703,862 |
| Dimensions | 2560x1600 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2016/02/allah-calligraphy-yellow-wallpaper.jpg |
| Capture | 2026-09-27T14:26:36+05:30 |
| Role in the post | `featured_media` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-2-2` (The Rationality of Believing in God Without Evidence — Part 2), `the-rationality-of-believing-in-god-without-evidence-part-1` (The Rationality of Believing in God Without Evidence — Part 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Arabic calligraphy of the name Allah in dark red on a textured yellow ground. |
| Alt text basis | written after viewing the image |

### `317_doubtskepticfinal.jpg`

| | |
|---|---|
| sha256 | `83b0a4d1f01b89b4126750c089728bde3a693f7570eaecc5001fbc69d0b59f25` |
| Bytes | 101,126 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2016/02/doubtskepticfinal.jpg |
| Capture | 2026-09-27T14:26:37+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-2-2` (The Rationality of Believing in God Without Evidence — Part 2) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Rationality of Believing in God Without Evidence — Part 2' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `318_gaston_la_touche_pardon_breton_1896.jpg`

| | |
|---|---|
| sha256 | `5b7e6cae1612f1282b6750cbe1588295bc56dedcd892b1c5383048d73979167a` |
| Bytes | 505,019 |
| Dimensions | 1024x924 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2016/02/gaston_la_touche_pardon_breton_1896.jpg |
| Capture | 2026-09-27T14:26:39+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-2-2` (The Rationality of Believing in God Without Evidence — Part 2) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Rationality of Believing in God Without Evidence — Part 2' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `319_inferior-mirage-1.png`

| | |
|---|---|
| sha256 | `133af3e3d3b62292a8b70eb789b4632135c2f3e2024132aa3d3e0e8206e19826` |
| Bytes | 17,068 |
| Dimensions | 996x652 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2016/02/inferior-mirage-1.png |
| Capture | 2026-09-27T14:26:40+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-2-2` (The Rationality of Believing in God Without Evidence — Part 2) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Rationality of Believing in God Without Evidence — Part 2' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `320_argumentsgod.jpg`

| | |
|---|---|
| sha256 | `2e2b349b9a20314c6463cad433e06f40c17e51e12afe095d3b6d7a200ad9f41a` |
| Bytes | 86,549 |
| Dimensions | 1282x772 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/08/argumentsgod.jpg |
| Capture | 2026-09-27T14:26:41+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-1` (The Rationality of Believing in God Without Evidence — Part 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Rationality of Believing in God Without Evidence — Part 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `321_figure3.jpg`

| | |
|---|---|
| sha256 | `e3d6b52e267c3dface7184b4d9daee8809853a2118121f8750387789cad505ee` |
| Bytes | 83,597 |
| Dimensions | 1280x720 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/08/figure3.jpg |
| Capture | 2026-09-27T14:26:43+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-1` (The Rationality of Believing in God Without Evidence — Part 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Rationality of Believing in God Without Evidence — Part 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `322_intuition.jpg`

| | |
|---|---|
| sha256 | `36c5f4ce3050d53ae877be8f19041a93f4888ef37694c3c11c24d60eaee44391` |
| Bytes | 33,819 |
| Dimensions | 758x484 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/08/intuition.jpg |
| Capture | 2026-09-27T14:26:44+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-rationality-of-believing-in-god-without-evidence-part-1` (The Rationality of Believing in God Without Evidence — Part 1) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Rationality of Believing in God Without Evidence — Part 1' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `323_fingerpointing-in-e14080318332322.jpg`

| | |
|---|---|
| sha256 | `241f9380eb1b8774e9fc91d0228cc9aaf89b98810f8d5ee3b91cbcf34be6fd93` |
| Bytes | 163,112 |
| Dimensions | 1553x1018 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/07/fingerpointing-in-e14080318332322.jpg |
| Capture | 2026-09-27T14:26:45+05:30 |
| Role in the post | `featured_media` |
| Work | `whataboutery` (‘Whataboutery': The Fail-Safe of Islamophobes) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with '‘Whataboutery': The Fail-Safe of Islamophobes' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `324_beautyimage.jpg`

| | |
|---|---|
| sha256 | `16b993688d9e77e01067fb3e6a9d6415760842c17bf9869d5714a0df101cc5a0` |
| Bytes | 481,146 |
| Dimensions | 818x654 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/06/beautyimage.jpg |
| Capture | 2026-09-27T14:26:46+05:30 |
| Role in the post | `featured_media` |
| Work | `the-archetype-of-beauty-in-islam-academic-article-independent` (The Archetype of Beauty in Islam) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'The Archetype of Beauty in Islam' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `325_saganevide.jpg`

| | |
|---|---|
| sha256 | `fa6ea84fa20a535b102ecbefb2e8ef5609332ecbf502062835133484855efd83` |
| Bytes | 74,084 |
| Dimensions | 850x400 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/05/saganevide.jpg |
| Capture | 2026-09-27T14:26:48+05:30 |
| Role in the post | `featured_media` |
| Work | `extraordinary-claims-require-extraordinary-evidence-says-ordinary-intellect` (“Extraordinary Claims Require Extraordinary Evidence”, Says Ordinary Intellect) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with '“Extraordinary Claims Require Extraordinary Evidence”, Says Ordinary Intellect' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `326_cafcaf-hebdo.jpg`

| | |
|---|---|
| sha256 | `c670ecc8c1da3c11f316138af6bd4657a4d0c91a4e7d9b423a3e13b36bb14099` |
| Bytes | 50,589 |
| Dimensions | 630x370 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/02/cafcaf-hebdo.jpg |
| Capture | 2026-09-27T14:26:50+05:30 |
| Role in the post | `featured_media` |
| Work | `charlie-hebdo-coexistence-and-crocodile-tears` (Charlie Hebdo, Coexistence and Crocodile Tears) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | The Charlie Hebdo cover cartoon “Nothing is forgiven”, showing caricatured men holding placards reading Syria, China, Gaza, Egypt, Afghanistan and Iraq. |
| Alt text basis | written after viewing the image |

### `327_091911-global-boko-haram1.png`

| | |
|---|---|
| sha256 | `616aa4979f70520a63d2d57bae77c4ee3ee946fc433e7f7262cd149e6e61945f` |
| Bytes | 991,703 |
| Dimensions | 1200x675 |
| Format | PNG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2014/05/091911-global-boko-haram1.png |
| Capture | 2026-09-27T14:26:52+05:30 |
| Role in the post | `featured_media` |
| Work | `boko-haram-and-the-culture-of-coercive-disapproval` (“Boko Haram” and the Culture of Coercive Disapproval) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | News photograph of masked armed men in camouflage standing on a boat. |
| Alt text basis | written after viewing the image |

### `328_abdal-hakim-murad-on-the-life-and-works-of-al-ghazali.jpg`

| | |
|---|---|
| sha256 | `47a64a88b663eb0c226888bd3ab0bbc292e26803b0bf224000d22177a7f1eee6` |
| Bytes | 101,992 |
| Dimensions | 1920x1080 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/05/abdal-hakim-murad-on-the-life-and-works-of-al-ghazali.jpg |
| Capture | 2026-09-27T14:26:53+05:30 |
| Role in the post | `featured_media` |
| Work | `supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad` (Supporting #HappyMuslims?: A Letter to Shaykh Abdal Hakim Murad) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Image recovered with 'Supporting #HappyMuslims?: A Letter to Shaykh Abdal Hakim Murad' from the author's own site. The recovered capture recorded the file but not what the image shows, so no subject is asserted here. |
| Alt text basis | generic, because the recovered capture does not record the image's subject |

### `330_168849_10150384646300089_2666639_n.jpg`

| | |
|---|---|
| sha256 | `38d7b36f100622283b0a0c85fc296c26fe08d6f09dbb1b4c5c352dbaf95b10b1` |
| Bytes | 68,165 |
| Dimensions | 720x540 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2014/04/168849_10150384646300089_2666639_n.jpg |
| Capture | 2026-09-27T14:26:57+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` (The Narrative of HappyMuslims: A Response to Adam Deen) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Two men standing on the carved stone balcony of an Andalusian-style building. |
| Alt text basis | written after viewing the image |

### `331_adam41.jpg`

| | |
|---|---|
| sha256 | `7b21afeef13e8d026ca93c90daaf0eb6e6a1d419bc2e9250186a60573a7e06b8` |
| Bytes | 15,940 |
| Dimensions | 451x136 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2014/04/adam41.jpg |
| Capture | 2026-09-27T14:26:58+05:30 |
| Role in the post | `text:bare-url` |
| Work | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` (The Narrative of HappyMuslims: A Response to Adam Deen) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of a Facebook post by Adam Deen about the #happymuslims video |
| Alt text basis | written after viewing the image |

### `332_adamdance.jpg`

| | |
|---|---|
| sha256 | `71e352741bc8cffab1a6da3d28f3c9e352e2b43235d495605ab05affe40f2dff` |
| Bytes | 49,788 |
| Dimensions | 739x330 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2014/04/adamdance.jpg |
| Capture | 2026-09-27T14:26:59+05:30 |
| Role in the post | `a:href+img:data-large-file+img:data-orig-file+img:src+img:srcset` |
| Work | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` (The Narrative of HappyMuslims: A Response to Adam Deen) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Video still of Adam Deen walking and gesturing along a park path. |
| Alt text basis | written after viewing the image |

### `333_honestypolicy1.jpg`

| | |
|---|---|
| sha256 | `3aeee276d99d7fb9da9d3cfb74d30233fa508636694dbabb3e36bc64f4dff605` |
| Bytes | 68,372 |
| Dimensions | 452x378 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2014/04/honestypolicy1.jpg |
| Capture | 2026-09-27T14:27:00+05:30 |
| Role in the post | `text:bare-url` |
| Work | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` (The Narrative of HappyMuslims: A Response to Adam Deen) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Screenshot of a Facebook post by The Honesty Policy reacting to a fabricated article about Shaykh Abdul Hakim Murad |
| Alt text basis | written after viewing the image |

### `334_happymuslim.jpg`

| | |
|---|---|
| sha256 | `8219438ef7cabf6db1c628adc6241013eb3beafff1d9011436249a55c14c1fc6` |
| Bytes | 289,696 |
| Dimensions | 1484x989 |
| Format | WEBP |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2015/05/happymuslim.jpg |
| Capture | 2026-09-27T14:27:01+05:30 |
| Role in the post | `featured_media` |
| Work | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` (The Narrative of HappyMuslims: A Response to Adam Deen) |
| Page | catalogued only |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | Press photograph of a crowd of young people dancing and clapping in a city square, filmed from below. |
| Alt text basis | written after viewing the image |

### `337_beautiful_lake_side_village_in_iceland.jpg`

| | |
|---|---|
| sha256 | `c9962a43de1017fbb857be6cd08092a11033ee270c2342d7b30989f28d54b8f1` |
| Bytes | 100,971 |
| Dimensions | 960x640 |
| Format | JPEG |
| Source URL | https://asadullahali.wordpress.com/wp-content/uploads/2011/12/beautiful_lake_side_village_in_iceland.jpg |
| Capture | 2026-09-27T14:27:06+05:30 |
| Role in the post | `featured_media` |
| Work | `thoughts-on-beauty` (Thoughts on Beauty) |
| Page | inline in the work page |
| Attribution | Published with this post on the author's own WordPress site; archived here for preservation with attribution to Asadullah Ali al-Andalusi. |
| Alt text | A snow-covered fishing village on a still fjord at dusk, its lit windows and red-and-white houses reflected in the water beneath snow-capped mountains. |
| Alt text basis | written after viewing the image |

## Per-work image map

Which images belong to which work. `Page` distinguishes the images inline on
the work's page from the ones only catalogued here.

| Work | Title | Images | Page inline | Catalogued only |
|---|---|---:|---:|---:|
| `a-muslims-guide-to-science-scientism` | A Muslim's Guide to Science: Scientism | 1 | 0 | 1 |
| `adam-is-no-myth` | Adam Is No “Myth” | 9 | 1 | 8 |
| `an-alternate-reality` | An Alternate Reality | 1 | 1 | 0 |
| `atheism-doubting-your-doubts` | Atheism: Doubting Your Doubts | 1 | 1 | 0 |
| `backbone-ribs` | Between a Backbone and Ribs: How Science Obscures the Beauty of the Qur’an | 3 | 1 | 2 |
| `boko-haram-and-the-culture-of-coercive-disapproval` | “Boko Haram” and the Culture of Coercive Disapproval | 1 | 0 | 1 |
| `charlie-hebdo-coexistence-and-crocodile-tears` | Charlie Hebdo, Coexistence and Crocodile Tears | 1 | 1 | 0 |
| `extraordinary-claims-require-extraordinary-evidence-says-ordinary-intellect` | “Extraordinary Claims Require Extraordinary Evidence”, Says Ordinary Intellect | 1 | 0 | 1 |
| `extremism-in-muslim-thought` | Extremism in Muslim Thought | 1 | 0 | 1 |
| `gods-mercy-without-eternal-punishment` | The Fire of God’s Mercy | 1 | 1 | 0 |
| `hard-questions-answering-doubts-about-islam` | Hard Questions: Answering Doubts About Islam | 1 | 1 | 0 |
| `ijihad-1` | iJihad 1 | 23 | 0 | 23 |
| `ikhalifa-ep-1` | iKhilafa (Episode 1) | 1 | 0 | 1 |
| `ikhalifa-ep-2` | iKhalifa Ep. 2 | 1 | 1 | 0 |
| `islam-and-litter-reduction` | Islam and Litter Reduction | 1 | 0 | 1 |
| `islam-and-terrorism` | Islam and Terrorism | 1 | 0 | 1 |
| `islam-science-and-history` | Islam, Science, and History | 1 | 1 | 0 |
| `liberalism-in-muslim-thought` | Liberalism in Muslim Thought | 1 | 0 | 1 |
| `liberalism-in-the-muslim-world` | Liberalism in the Muslim World | 1 | 0 | 1 |
| `lost-in-time-translation` | Lost in Time-Translation | 1 | 1 | 0 |
| `my-views-on-the-punishment-for-apostasy` | My Views On the Punishment For Apostasy | 3 | 1 | 2 |
| `naked-kings-in-the-information-age` | Naked Kings in the Information Age | 1 | 1 | 0 |
| `of-context-and-confusion` | Of Context and Confusion | 1 | 1 | 0 |
| `reviewing-haqiqatjou` | The Dishonesty of Daniel Haqiqatjou – Don Quixote de la Ummah | 206 | 1 | 205 |
| `supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad` | Supporting #HappyMuslims?: A Letter to Shaykh Abdal Hakim Murad | 1 | 0 | 1 |
| `the-archetype-of-beauty-in-islam-academic-article-independent` | The Archetype of Beauty in Islam | 1 | 0 | 1 |
| `the-atheistic-worldview-vs-the-quranic-worldview` | The Atheistic Worldview vs. The Qur’anic Worldview | 1 | 1 | 0 |
| `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` | The Narrative of HappyMuslims: A Response to Adam Deen | 5 | 2 | 3 |
| `the-quran-science-a-forced-marriage` | The Quran, Science: A Forced Marriage | 1 | 0 | 1 |
| `the-rationality-of-believing-in-god-without-evidence-part-1` | The Rationality of Believing in God Without Evidence — Part 1 | 4 | 0 | 4 |
| `the-rationality-of-believing-in-god-without-evidence-part-2-2` | The Rationality of Believing in God Without Evidence — Part 2 | 4 | 0 | 4 |
| `the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables` | The Structure of Scientific Productivity in Islamic Civilization: Orientalists’ Fables | 1 | 0 | 1 |
| `thoughts-on-beauty` | Thoughts on Beauty | 1 | 1 | 0 |
| `understanding-aishas-age-an-interdisciplinary-approach` | Understanding Aisha’s Age: An Interdisciplinary Approach | 1 | 1 | 0 |
| `understanding-atheism` | Understanding Atheism | 1 | 1 | 0 |
| `whataboutery` | ‘Whataboutery': The Fail-Safe of Islamophobes | 1 | 0 | 1 |
| `when-religion-becomes-confusing` | When Religion Becomes Confusing | 1 | 0 | 1 |
| `yolo-a-motto-of-ignorance` | #YOLO: A Motto of Ignorance | 1 | 1 | 0 |

The 26 image references that existed in the recovered content are all
resolved: 21 rewired to a local path under `/andalusian-archive/assets/images/`
and 5 marked as not recovered. Twenty-three were markdown images; three were
bare image URLs sitting in reader-facing prose (endnotes in
`the-narrative-of-happymuslims` and `a-quick-response`) and were rewired in
place so no remote image host is left in the rendered text. The other 263 published files are images the
original posts carried but whose position inside the prose the recovered
capture did not preserve (lane F1 extracted post text, and `<img>`
contributes no text). They are catalogued here rather than placed in the
prose at invented positions, which is why the two largest sets - the 206
images of `reviewing-haqiqatjou` and the 23 comic plates of `ijihad-1` -
appear in the table above but not inline in the work text.

## Deduplicated duplicates

Lane F1 staged both the `src` re-upload and the `data-orig-file` original of
the same picture, so every referenced URL resolved to a file. The groups
below are byte-identical. The lowest-numbered file of each group is the one
published; the rest are recorded here and dropped.

| Dropped file | Published instead | sha256 (shared) | Bytes |
|---|---|---|---:|
| `037_21d39-readinglist.jpg` | `025_1b171-readinglist.jpg` | `f69bd42a0626083033aad050dd8fae2debf37be5d17d44d7a97ef4cdeb020efe` | 73,853 |
| `053_36da4-hijab3-1.jpg` | `006_04292-hijab3-1.jpg` | `9389a538d4dec383ecc5efa48d87d6dbb28c583eb6ac22438e17c5674345c0e3` | 111,048 |
| `063_3f5ef-salvationcritic1.jpg` | `010_0c79d-salvationcritic1.jpg` | `ea0759d81c7852916c776f4167669fe853739304f4c87865a42856a259959e91` | 97,381 |
| `073_49790-gouda.jpg` | `021_19229-gouda.jpg` | `bcea44bd9c68e920ba38abada4c3484eee8d00a545e06ecf52e56dee72ec479f` | 77,528 |
| `107_63f71-unseenarabic2.jpg` | `097_5c98b-unseenarabic2.jpg` | `91b29aa74cd7db712d270c2cf31f8f50dc7e4fcfb8f39efcc2e7f10230ffc4eb` | 41,289 |
| `121_76eba-hijab9.jpg` | `118_735d0-hijab9-1.jpg` | `37c5c52b2b0a7d4d6bc5c4f884fcc9249e35a777c09a41573412e5a1d8290f49` | 107,571 |
| `128_7cca0-hijab9-1.jpg` | `118_735d0-hijab9-1.jpg` | `37c5c52b2b0a7d4d6bc5c4f884fcc9249e35a777c09a41573412e5a1d8290f49` | 107,571 |
| `136_88725-modeltitle3.jpg` | `057_39a4e-modeltitle3.jpg` | `0f6e1f2b44dd4b025ee01496557aa2a31617e2df3033a6b7b76ebc15065295aa` | 136,129 |
| `137_8b7ed-2.png` | `062_3ef70-2.png` | `67cd1d6aadcb8ed8099137184f235f4781ef1b1dd7bffb8c97bf1a75b5e3423b` | 35,347 |
| `141_930f0-danielhaya1-2.jpg` | `054_371c0-danielhaya1-2.jpg` | `95e2b4b8d7ca9b00d9a177cf9762f3c2d6024d11c411b26dac72f258c266120d` | 179,465 |
| `142_932e0-convo1.jpg` | `022_19feb-convo1.jpg` | `0b22219d71bda11901d0e83a1e0bdf6d9ea4b90c20f23a8060d87479b63c2344` | 215,054 |
| `147_97da4-danielhaya14.jpg` | `004_01f91-danielhaya14.jpg` | `a87a15cc0c6c7b1a2f8d18964342e8a7f7eee5b46b3dfce2657203e77d318439` | 163,814 |
| `148_98013-dantweet1-1.jpg` | `016_12266-dantweet1-1.jpg` | `1d2274b658f6b7f5464145df0a9bb40dab3185b8d08ba0bc19117099d7b8aed6` | 104,404 |
| `154_9b29e-hijab7-1.jpg` | `109_6883e-hijab7-1.jpg` | `12af7faf5a61367258560d6b77695473cbe921888a221f7089c0f95412fd40f6` | 112,319 |
| `158_9d6f4-danielhaya6.jpg` | `144_947a8-danielhaya6.jpg` | `cd6f31f33b9559c9a185f2fda7612019225ae9be3f1dfafd3fb294f3448d9d2e` | 143,328 |
| `160_9f861-danielhaya15.jpg` | `013_0edee-danielhaya15.jpg` | `1854880796a0ed9c039133fc777bc585f0aa0db57cd7e168c0e0490d5021bcfd` | 158,494 |
| `163_a1dcf-readinglist4.jpg` | `146_9555c-readinglist4.jpg` | `bf5e695c38a51b0366c8b6db402bea1d183f9953d52a0ebdd6ddf189fd8d42e5` | 130,078 |
| `168_a8746-unseen3.jpg` | `159_9f6a7-unseen3.jpg` | `38f849b852c83dfa9f8177b9c616615aff36aa183af09a889423fa270d5e0e36` | 34,989 |
| `170_a96b9-danielhaya3.jpg` | `080_4df1d-danielhaya3.jpg` | `5b2dcb788008dfb9970a998760e4a3d81c61902611b61afe80d3f804a9e2126a` | 156,237 |
| `172_a9b1a-unseenarabic.jpg` | `058_3abbc-unseenarabic.jpg` | `77f415524972bcf5fc31b96b827b058f2b35e142af06994da968ff6204e6994e` | 48,218 |
| `174_ab960-danielhaya7.jpg` | `104_608e3-danielhaya7.jpg` | `14fb602db029d91eb69c0213ab9cd2812c2de19e2047b77f84995de5915d1759` | 114,472 |
| `177_ad54a-convo2.jpg` | `036_204cb-convo2.jpg` | `9639c29bb43ac1580a286ade4b6b13c9c8a1bac83460051fcfb58a5acbf551d3` | 163,719 |
| `179_aef77-hijab2-1.jpg` | `094_5a188-hijab2-1.jpg` | `8ee38e0da119bf4e9596f2aca4722b0fa9eea981e809790951e041f5fff1df13` | 133,467 |
| `180_af2eb-danielhaya13.jpg` | `028_1c755-danielhaya13.jpg` | `63e23c083c13ff434e0283621f38d49a24b0a264638b6a1ee3e70012810937ee` | 187,638 |
| `183_b3fbd-danielhaya18.jpg` | `055_386b1-danielhaya18.jpg` | `7525d0638273d4524c1859e27955140d2d3c0b856822b7e5d8f66a196d64d52b` | 85,107 |
| `184_b51a3-danielhaya8.jpg` | `127_7cb1a-danielhaya8.jpg` | `736f6637039d9c43d8fce16b2a6cf2b5c4494e13e23ff1abc38684fd540cc8ef` | 124,061 |
| `185_b6670-danielhaya19.jpg` | `075_4a451-danielhaya19.jpg` | `c6ff07e406c46241d47973bc3a2e7be1848db547cf73287d47e215c9bc079ca9` | 93,790 |
| `188_b832d-convo8.jpg` | `008_0b4c6-convo8.jpg` | `803da40a34cb00f19923f86b3e6c5635280b14101217c9f1160aa09f3b2fe2a4` | 140,236 |
| `189_b989b-danielhaya12.jpg` | `012_0d132-danielhaya12.jpg` | `f94b66f65c91fcc42fa20a92b983251361f5c1c19197167b0e8f6d437b159ffe` | 136,117 |
| `194_c1056-danielhaya5.jpg` | `085_51eb9-danielhaya5.jpg` | `00352f27055d81ec527f8ebf5bf3bc2e46b23d1982231f17d1d94a7c45d7be61` | 72,141 |
| `204_c6fd6-danielhaya11.jpg` | `110_68da4-danielhaya11.jpg` | `c58c59d1ea1e3676f02ef5debd2b30cdf079975fe8250253af30cb529ea0664f` | 168,140 |
| `209_cc1b2-hijab6-1.jpg` | `182_b2348-hijab6-1.jpg` | `c6904aaaee2ec61dc04872d901b5fcbb577641457326a2d4b98cf49d526f7028` | 105,448 |
| `211_cd5fd-danielhaya20.jpg` | `078_4c8c2-danielhaya20.jpg` | `2bdf394db850c6f3a022bb9b3d4173f90457a8e7a632d7fb6ee4caa2e9ad8ebf` | 155,242 |
| `217_d25e4-orientalistseditors1.jpg` | `113_6f368-orientalistseditors1.jpg` | `d8a3e358eb6cacc89fa5e214910ffb4295b7895aa9135e521cba51df9fb3c807` | 50,765 |
| `221_d5f59-danielhaya22.jpg` | `212_cddb8-danielhaya22.jpg` | `66a1457eba0d9563bc7412403ff1b2a697b37a877c9a8fbc48df4e13d5417535` | 133,577 |
| `222_d6177-specialthanks-1.jpg` | `005_03a67-specialthanks-1.jpg` | `3349800f1a342f00ad89c2aeb01b09a15d4d76880258686b7346203414310f73` | 253,281 |
| `225_d9220-slack3.jpg` | `161_9fd10-slack3.jpg` | `66063923b5282e2e9652936c204bd2769cb74e017198ee2569abb60b95a3d5f8` | 342,553 |
| `226_da03d-salvationcritic2.jpg` | `150_988c9-salvationcritic2.jpg` | `8186d326f426759edb69cf9af25a924f93d878463ed2d90883653e0f24616a58` | 132,110 |
| `227_dc4a2-hijab8-1.jpg` | `210_cc3a2-hijab8-1.jpg` | `643268bfaafa412b9c2a60b597d26fdde7489874b9ed0dfbf1708b1e1e14aab9` | 94,419 |
| `233_eb7f4-convo3.jpg` | `201_c656e-convo3.jpg` | `270dde0cae73d4096461b7bb44ebb10176df57e91df7a98ab388546dc89f9da9` | 242,784 |
| `239_eec9b-update1.jpg` | `081_4ecda-update1.jpg` | `591638f172d8e417f2a0690e41d645fa57fc223e9d9b3257cb08352fbded6f1b` | 378,379 |
| `241_f0bbb-danielhaya4.jpg` | `014_0f451-danielhaya4.jpg` | `3ec0371111608ee29bccb7d01bc2cf8e4521f3afbbec4fa04c564ba4015f1882` | 139,479 |
| `242_f305c-danielhaya17.jpg` | `165_a625c-danielhaya17.jpg` | `be91376632a0ea7041910b7791e2b5e14db9c83b47f534c5aed3ca67e8fe2d3a` | 113,039 |
| `246_f9ef3-hijab5-1.jpg` | `048_312e5-hijab5-1.jpg` | `0245482745f1e706dda5bae7ac3761195be02c52e28dde929f821412fcc29efd` | 116,960 |
| `250_fd0be-albanialmufrad.jpg` | `017_145dd-albanialmufrad.jpg` | `c489c002283d83cf48dc17d6a2e6975be5abf5c7fb48746562566ebe70eec32b` | 14,993 |
| `252_fe42a-hijab9.jpg` | `118_735d0-hijab9-1.jpg` | `37c5c52b2b0a7d4d6bc5c4f884fcc9249e35a777c09a41573412e5a1d8290f49` | 107,571 |
| `254_fedbf-hijab4-1.jpg` | `091_588c4-hijab4-1.jpg` | `9fe5d3316cefd39127cd8bb79cd9e89659a44a7cdc9a48d0fa0a27626eb5cd69` | 134,298 |
| `255_fee77-readinglist1.jpg` | `119_75812-readinglist1.jpg` | `9295e5661d34dbc7143c19c4242e826020382ae615c20b7c164d4425d5ae2419` | 209,045 |
| `257_ff573-danielhaya16.jpg` | `106_63f14-danielhaya16.jpg` | `f430b32f7f17794eeabcb8edd9c2c6fd13db84b560cd99ccf8c239c22ba157bd` | 157,972 |

Groups containing more than two files: `118_735d0-hijab9-1.jpg`,
`121_76eba-hijab9.jpg`, `128_7cca0-hijab9-1.jpg` and `252_fe42a-hijab9.jpg`
are four copies of one image; `118_` is published.

## Not published

| Staged file | Bytes | Why it is not in `assets/images/` |
|---|---:|---|
| `backboneribspdf-2.pdf` | 2,534,058 | A PDF, not an image. Held per the lane brief. It is the author-hosted copy of *Between a Backbone and Ribs*; source URL `https://asadullahali.wordpress.com/wp-content/uploads/2020/01/backboneribspdf-2.pdf`. |
| `258_Symbol2.5.jpg` | 135,660 | **Not an image.** The URL `https://atomic-temporary-15984398.wpcomstaging.com/wp-content/uploads/2020/06/Symbol2.5.jpg` is a WordPress *staging* host hard-coded in the post body; it answered HTTP 200 with a 135,660-byte HTML page, so lane F1 recorded a successful capture of XHTML. Publishing it would have shipped a broken image. |

## Unrecoverable references

Five image references in the published works cannot be satisfied. None is
left pointing at a remote host; each is replaced on the page by a visible
`> **Image not recovered.**` marker naming the file.

| Reference | Where it appears | Origin | Failure |
|---|---|---|---|
| `endowment-democracy-exit-national.si.jpg` | `_posts/2014-02-16-malaysias-tiger-in-waiting.md` | `img.rt.com` | Hot-linked from a third-party news site rather than hosted with the post, so it was never in the mirror plan and no copy exists here. |
| `pamelageller_mugshot_four_by_three_s267x200.jpg` | `_posts/2014-04-30-the-narrative-behind-happymuslims.md` | `media.washtimes.com` via the `i0.wp.com` image proxy | HTTP 403 from the proxy after 2 retries. A newspaper mugshot of a private individual; it would have been withheld under the privacy rule even had it been captured. |
| `breakdance-CypherSessions.jpg` | `_posts/2014-04-30-the-narrative-behind-happymuslims.md` | `www.famemagazine.co.uk` via `i0.wp.com` | HTTP 404: the proxy had no cached copy and the origin page was gone. |
| `malaymail.jpg` | `_posts/2016-04-30-how-feminism-undermines-islam-and-gender-justice.md` | the author's own site | The post falls outside the 38 posts lane F1 mirrored, so the file was never requested. |
| `understand.jpg` | `_posts/2014-06-10-a-quick-response.md` | the author's own site | Endnote [3] cited the file as a bare URL in the prose. Same cause: the post falls outside the mirrored set. |

A further three image URLs were recorded by lane F1 as failures and never
had a staged file, so they have no reference in the recovered text to mark:

| Origin URL | Referenced by | Status |
|---|---|---|
| `https://i0.wp.com/www.skibbereeneagle.ie/web/wp-content/uploads/2014/04/happyvideo-was-create.jpg` | `supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad` | HTTP 404 |
| `https://i0.wp.com/media.washtimes.com/media/image/2013/06/27/pamelageller_mugshot_four_by_three_s267x200.jpg` | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` | HTTP 403 |
| `https://i0.wp.com/www.famemagazine.co.uk/wp-content/uploads/2010/09/breakdance-CypherSessions.jpg` | `the-narrative-of-happymuslims-a-response-to-adam-deen-and-the-honesty-policy` | HTTP 404 |

## Withheld

**Nothing was withheld.** No image in this set is a photograph of a private
individual rather than the author's own material. The reasoning, and the
images actually opened and looked at, are recorded in
`.superpowers/sdd/2026-09-27-full-recovery-v6/pub-P3-report.md`. In short:

- The people who appear are named public figures whose own published work is
  under discussion - Daniel Haqiqatjou, the subject of the review; Adam
  Deen and Rameez Abid, the subjects of the pieces they appear in; Dr David
  Jalajel, the author of *Adam is No Myth*; the hosts of public channels the
  author interviewed.
- Most of the human-bearing files in the largest set are not photographs of
  people at all. They are screenshots of public text: Facebook and YouTube
  post captures, memes, and article and PDF-page screenshots. Those are
  documents, and capturing them is the point of the archive.
- Two images show groups of people in public places with no individual
  identifiable from the file: a press photograph of a crowd dancing in a
  city square, and a news photograph of masked armed men on a boat.
- One image, `330_168849_10150384646300089_2666639_n.jpg`, shows two men on
  a balcony of a heritage building and the subjects could not be established
  from the file. It is a still from the *Happy Muslims* video that the post
  argues about, re-hosted on a Facebook CDN, and it was published by the
  author in this article. It is published here for that reason, and it is
  flagged here so the judgement is visible rather than silent.
- `046_2ffde-dhcover3.jpg` is the author's own montage placing a
  cut-out photograph of Daniel Haqiqatjou beside a graffitied windmill. It
  is defamatory in tone, it is the cover image of the work, and it is
  preserved unaltered.

## Known defects in the published set

| File | Defect |
|---|---|
| `334_happymuslim.jpg` | The bytes are WebP, the extension is `.jpg`. It renders correctly in every current browser (images are content-sniffed) but a server sends it as `image/jpeg`. The extension was kept so the published name still matches the source URL's basename and the provenance column stays checkable. |
| `258_Symbol2.5.jpg` | Excluded above: an HTML page fetched under an image name. |
| `reviewing-haqiqatjou` image set | 207 files, 30.1 MB, published but not inline. The page itself carries only the one image reference the recovered text preserved. |

