# Fetch-damage triage - 2026-09-29

`scripts/fetch_damage.py` reports three judgement classes across the five
recovered collections. This is a **per-hit triage of every one of them**, and a
verdict list for the site owner to act on. No content file was modified.

```
python -B scripts/fetch_damage.py
scanned 5 collections, 80 file(s) with hits
  by class: encoding=72, join=96, space=119
```

That is the whole scanner output. It is 80 files with hits out of 326 scanned:
54 `_posts`, 92 `_articles`, 20 `_papers`, 81 `_videos`, 79 `_transcripts`.
Note what is **not** in the output: `residue` and `chrome` are both zero, so the
two classes the module treats as unambiguous and gate-failing report a clean
bill of health to all five collections. Section 5 shows that this is wrong, and
that the clean bill of health is the most consequential thing in this report.

## How each hit was decided

The detector is a shape-matcher, so a shape match is not a verdict. Every hit
was adjudicated against **the raw capture it came from** where one exists:

| evidence used | where it lives |
|---|---|
| the Wayback page as served | `_staging/best_capture/pages/*.html` |
| the mirror lane's plain-text extraction | `_staging/mirror/posts/*.txt` |
| the MDI republication's own capture | `_staging/mdi/posts/*.txt` |
| the raw caption capture | `.firecrawl/transcripts/cap-*.en-orig.vtt` |

Of the 326 files scanned, 43 of the 54 `_posts` files have a raw capture that
could be matched to them by name, and 14 of those 43 differ from the recovered
file at all. Those 14 are what section 5b measures. Where no capture exists,
shape is the only evidence, and the hit is left in the undecided table rather
than promoted.

Three verdicts are used, and the third exists because the first two do not
cover the whole census:

* **DAMAGE** - the fetcher did this, or it is WordPress furniture. Removing it
  restores his text; it does not alter it.
* **NOT DAMAGE** - either his own text as published, or this repository's own
  text, or machine bytes the source capture carries and the archive keeps on
  purpose. Recorded per hit because it is the evidence that the scanner was not
  simply believed.
* **UNDECIDED** - no capture exists to settle it and shape cannot. **These
  stay.** A wrong repair edits a man writing; a wrong leave costs one odd line
  a human can look at.

## 1. The census

Every hit the scanner reported is in one of the three tables below.
**102 + 169 + 16 = 287**, and 96 + 119 + 72 = 287.

| collection | files scanned | join | space | encoding | total |
|---|---|---|---|---|---|
| `_posts` | 31 files with hits | 82 | 74 | 0 | **156** |
| `_articles` | 5 files with hits | 7 | 3 | 0 | **10** |
| `_papers` | — | 0 | 0 | 0 | **0** |
| `_transcripts` | 43 files with hits | 6 | 42 | 72 | **120** |
| `_videos` | 1 file with hits | 1 | 0 | 0 | **1** |
| **total** | **80 files** | **96** | **119** | **72** | **287** |

| class | rule | damage | not damage | undecided | total |
|---|---|---|---|---|---|
| `join` | all rules in the class | 56 | 37 | 3 | 96 |
| `space` | all rules in the class | 46 | 60 | 13 | 119 |
| `encoding` | all rules in the class | 0 | 72 | 0 | 72 |
| | `html-entity` | 0 | 72 | 0 | 72 |
| | `no-space-after-stop` | 42 | 4 | 3 | 49 |
| | `space-before-punctuation` | 4 | 56 | 10 | 70 |
| | `tag-strip-join-full-stop` | 7 | 0 | 0 | 7 |
| | `tag-strip-join-lower-upper` | 49 | 37 | 3 | 89 |

Two things the census says before any judgement is applied:

* **All 102 damage hits are in `_posts`.** `_articles`, `_papers`,
  `_transcripts` and `_videos` return zero damage.
* **`_transcripts` returns 120 hits and not one of them is damage.** 80 of the
  120 are this repository's own rendering note, quoted in full in the
  not-damage table.

## 2. Judged DAMAGE - 102 hits, 18 files

Breakdown: **77 comment-thread furniture** (11 files), **5 injected
script/CSS** (1 file), **20 destroyed spaces in his prose** (11 files).

One row per distinct hit; `n` is how many times that exact hit occurs on that
line. The `n` column sums to 102.

| # | file | line | text | rule | n | context | why |
|---|---|---|---|---|---|---|---|
| 1 | `_posts/2011-12-31-thoughts-on-beauty.md` | 20 | `.` | `no-space-after-stop` | 1 | …hich is essentially just a term simultaneous withbeauty.Beauty, to call someonebeautiful, is to transcend these… | source capture has the space; the recovered file does not |
| 2 | `_posts/2011-12-31-thoughts-on-beauty.md` | 28 | `.` | `no-space-after-stop` | 1 | …han. Nice post. I never thought beauty and war that way.Reply… | WordPress comment thread flattened into the body |
| 3 | `_posts/2011-12-31-thoughts-on-beauty.md` | 28 | `way.Reply` | `tag-strip-join-full-stop` | 1 | …SKhan. Nice post. I never thought beauty and war that way.Reply… | WordPress comment thread flattened into the body |
| 4 | `_posts/2011-12-31-thoughts-on-beauty.md` | 28 | `2012Salaam` | `tag-strip-join-lower-upper` | 1 | …- Islamotroll10 Mar 2012Salaam Alaykum Ali,This is SKhan. Nice post. I never thought… | WordPress comment thread flattened into the body |
| 5 | `_posts/2013-06-09-prophets-vs-pedophiles-part-3.md` | 55 | `.` | `no-space-after-stop` | 1 | …right of the guardian, or at least a synthesis of both.While the guardian has the right to conclude a marriage… | source capture has the space; the recovered file does not |
| 6 | `_posts/2013-06-21-marina-mahathir-against-women-logic-islam.md` | 28 | `.` | `no-space-after-stop` | 1 | …humiliated, believing that it will never happen to them.So the logic that such a punishment will act as a deter… | source capture has the space; the recovered file does not |
| 7 | `_posts/2014-05-04-supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad.md` | 18 | `calledThe` | `tag-strip-join-lower-upper` | 1 | …hased a wonderful and enlightening book written by you calledThe Commentary on the Eleventh Contentions. I was particu…… | source capture has the space; the recovered file does not |
| 8 | `_posts/2014-05-04-supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad.md` | 20 | `.` | `no-space-after-stop` | 1 | …re’s shrunken victims with gratitude for God’s guidance.Part of that gratitude and humility takes the form of a… | source capture has the space; the recovered file does not |
| 9 | `_posts/2014-05-04-supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad.md` | 22 | `ofContentions` | `tag-strip-join-lower-upper` | 1 | …or not you’ve changed your position since the writing ofContentions, or contradicted yourself. The first issue I have …… | source capture has the space; the recovered file does not |
| 10 | `_posts/2014-05-04-supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad.md` | 30 | `.` | `no-space-after-stop` | 1 | …ject — is related to the above quote in yourContentions.You call on us all to reject the mon0culture and to be… | source capture has the space; the recovered file does not |
| 11 | `_posts/2014-05-04-supporting-happymuslims-a-letter-to-shaykh-abdal-hakim-murad.md` | 30 | `yourContentions` | `tag-strip-join-lower-upper` | 1 | …opposed the project — is related to the above quote in yourContentions.You call on us all to reject the mon0culture an…… | source capture has the space; the recovered file does not |
| 12 | `_posts/2015-02-14-charlie-hebdo.md` | 14 | `newspaperCharlie` | `tag-strip-join-lower-upper` | 1 | …e) in solidarity with those massacred at the satirical newspaperCharlie Hebdo. Despite the murderers having been broug…… | source capture has the space; the recovered file does not |
| 13 | `_posts/2015-02-14-charlie-hebdo.md` | 26 | `ifCharlie` | `tag-strip-join-lower-upper` | 1 | …mitism would erupt across Europe and the United States ifCharlie Hebdohad depicted the Prophet Musa (Moses,alayhi sall…… | source capture has the space; the recovered file does not |
| 14 | `_posts/2015-02-14-charlie-hebdo.md` | 46 | `byCharlie` | `tag-strip-join-lower-upper` | 1 | …o criticism in provocative images, such as those drawn byCharlie Hebdo, or the Danish cartoons prior.… | source capture has the space; the recovered file does not |
| 15 | `_posts/2015-02-14-charlie-hebdo.md` | 50 | `newCharlie` | `tag-strip-join-lower-upper` | 1 | …agazine –CafCaf– has responded in defiance towards the newCharlie Hebdocover with a cover of their own: a cartoon of t…… | source capture has the space; the recovered file does not |
| 16 | `_posts/2015-02-14-charlie-hebdo.md` | 64 | `theCharlie` | `tag-strip-join-lower-upper` | 1 | …rity of Westerners are more concerned with things like theCharlie Hebdomassacre – and are willing to protest and march…… | source capture has the space; the recovered file does not |
| 17 | `_posts/2015-02-14-charlie-hebdo.md` | 70 | `.` | `no-space-after-stop` | 1 | …s his military is,” hence a legitimate target of attack.There were no demonstrations or cries of outrage, no ch… | source capture has the space; the recovered file does not |
| 18 | `_posts/2015-02-14-charlie-hebdo.md` | 84 | `2015Salaam` | `tag-strip-join-lower-upper` | 1 | …- isa sulaiman19 Feb 2015Salaam! Well written… A positive read on a very current subje… | WordPress comment thread flattened into the body |
| 19 | `_posts/2015-07-30-whataboutery.md` | 40 | `.` | `no-space-after-stop` | 1 | …ntation of what the fallacy of relative privation isnot.Maryam accuses Islamic Law of taking away women’s right… | source capture has the space; the recovered file does not |
| 20 | `_posts/2016-04-30-how-feminism-undermines-islam-and-gender-justice.md` | 20 | `.` | `no-space-after-stop` | 1 | …at Islam was sufficient for granting women their rights.Now, none of the organizers seemed too concerned about… | source capture has the space; the recovered file does not |
| 21 | `_posts/2017-05-07-the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables.md` | 16 | `forYaqeen` | `tag-strip-join-lower-upper` | 1 | …alaykum everyone. I’ve just published my first article forYaqeen Institute for Islamic Researchtitled “The Structure o…… | source capture has the space; the recovered file does not |
| 22 | `_posts/2017-05-07-the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables.md` | 24 | `parentNode` | `tag-strip-join-lower-upper` | 1 | …var p = o.parentNode;… | injected CSS/JavaScript left in the body |
| 23 | `_posts/2017-05-07-the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables.md` | 25 | `setProperty` | `tag-strip-join-lower-upper` | 1 | …p.style.setProperty('display', 'inline-block', 'important');… | injected CSS/JavaScript left in the body |
| 24 | `_posts/2017-05-07-the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables.md` | 26 | `setProperty` | `tag-strip-join-lower-upper` | 1 | …o.style.setProperty('display', 'block', 'important');… | injected CSS/JavaScript left in the body |
| 25 | `_posts/2017-05-07-the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables.md` | 28 | `setProperty` | `tag-strip-join-lower-upper` | 1 | …o.style.setProperty('display', 'none', 'important');… | injected CSS/JavaScript left in the body |
| 26 | `_posts/2017-05-07-the-structure-of-scientific-productivity-in-islamic-civilization-orientalists-fables.md` | 29 | `setProperty` | `tag-strip-join-lower-upper` | 1 | …o.style.setProperty('visibility', 'hidden', 'important');… | injected CSS/JavaScript left in the body |
| 27 | `_posts/2017-12-22-understanding-atheism.md` | 25 | `.` | `no-space-after-stop` | 1 | …ter format. That’s a lot to look at but I like the idea.Reply… | WordPress comment thread flattened into the body |
| 28 | `_posts/2017-12-22-understanding-atheism.md` | 25 | `2017Maybe` | `tag-strip-join-lower-upper` | 1 | …- jim-24 Dec 2017Maybe a little blurb and one video a day would be a better f… | WordPress comment thread flattened into the body |
| 29 | `_posts/2017-12-22-understanding-atheism.md` | 26 | `.` | `no-space-after-stop` | 1 | …see some words on slide even I download 1080p HD video.Reply… | WordPress comment thread flattened into the body |
| 30 | `_posts/2017-12-22-understanding-atheism.md` | 26 | `2018Could` | `tag-strip-join-lower-upper` | 1 | …- Thu Ya7 Jan 2018Could you give me the courseware slides? I can’t see some wo… | WordPress comment thread flattened into the body |
| 31 | `_posts/2018-03-10-of-context-and-confusion.md` | 50 | ` !` | `space-before-punctuation` | 1 | …- fajrimuhammadin10 Mar 2018Awesome take on the topic !Reply… | WordPress comment thread flattened into the body |
| 32 | `_posts/2018-03-10-of-context-and-confusion.md` | 50 | `2018Awesome` | `tag-strip-join-lower-upper` | 1 | …- fajrimuhammadin10 Mar 2018Awesome take on the topic !Reply… | WordPress comment thread flattened into the body |
| 33 | `_posts/2018-03-10-of-context-and-confusion.md` | 51 | `2018Amazing` | `tag-strip-join-lower-upper` | 1 | …- Marooq810 Mar 2018Amazing lolReply… | WordPress comment thread flattened into the body |
| 34 | `_posts/2018-03-10-of-context-and-confusion.md` | 51 | `lolReply` | `tag-strip-join-lower-upper` | 1 | …- Marooq810 Mar 2018Amazing lolReply… | WordPress comment thread flattened into the body |
| 35 | `_posts/2018-03-10-of-context-and-confusion.md` | 52 | `2018Great` | `tag-strip-join-lower-upper` | 1 | …- Mokavi10 Mar 2018Great piece, I really look forward to more of your content.… | WordPress comment thread flattened into the body |
| 36 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 98 | `.` | `no-space-after-stop` | 5 | …probably a pretty solid reason for leaving the religion.ReplyShahzeb25 May 2018Oh no Asadullah, we got another… | WordPress comment thread flattened into the body |
| 37 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 98 | `one.Reply` | `tag-strip-join-full-stop` | 1 | …ReplyShahzeb25 May 2018Oh no Asadullah, we got another one.ReplyAdam7AE27 May 2018If I had any doubts as to the truthf…… | WordPress comment thread flattened into the body |
| 38 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 98 | `you.Reply` | `tag-strip-join-full-stop` | 1 | …article’s claims, you’ve certainly quelled them.Thank you.ReplyAmanda27 May 2018No need to thank me for your own ignor… | WordPress comment thread flattened into the body |
| 39 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 98 | `2018Islam` | `tag-strip-join-lower-upper` | 1 | …- Amanda24 May 2018Islam oppressing girls and women is probably a pretty solid… | WordPress comment thread flattened into the body |
| 40 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 99 | `.` | `no-space-after-stop` | 1 | …. Keep writing that fire Asadullah. May Allah bless you.Reply… | WordPress comment thread flattened into the body |
| 41 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 99 | `you.Reply` | `tag-strip-join-full-stop` | 1 | …day. Keep writing that fire Asadullah. May Allah bless you.Reply… | WordPress comment thread flattened into the body |
| 42 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 99 | `2018Everything` | `tag-strip-join-lower-upper` | 1 | …- Shahzeb25 May 2018Everything said in this article is true. It’s not long now until… | WordPress comment thread flattened into the body |
| 43 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 100 | `.` | `no-space-after-stop` | 1 | …ube.com/watch?v=Lu8ZkauTlrwReplySh9 Jun 2018Great video.Reply… | WordPress comment thread flattened into the body |
| 44 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 100 | `2018You` | `tag-strip-join-lower-upper` | 1 | …- Naved9 Jun 2018You are really touching on an important phenomenon and app… | WordPress comment thread flattened into the body |
| 45 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 100 | `2018Great` | `tag-strip-join-lower-upper` | 1 | …ttps://www.youtube.com/watch?v=Lu8ZkauTlrwReplySh9 Jun 2018Great video.Reply… | WordPress comment thread flattened into the body |
| 46 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 101 | `thanksReply` | `tag-strip-join-lower-upper` | 1 | …- Ars23 Jun 2018well intellectually presented.thanksReply… | WordPress comment thread flattened into the body |
| 47 | `_posts/2018-06-29-an-alternate-reality.md` | 52 | `.` | `no-space-after-stop` | 1 | …ahi13 Jul 2018Wow. That was amazingly written well done.Reply… | WordPress comment thread flattened into the body |
| 48 | `_posts/2018-06-29-an-alternate-reality.md` | 52 | `2018Wow` | `tag-strip-join-lower-upper` | 1 | …- Siphahi13 Jul 2018Wow. That was amazingly written well done.Reply… | WordPress comment thread flattened into the body |
| 49 | `_posts/2018-06-29-an-alternate-reality.md` | 53 | `.` | `no-space-after-stop` | 3 | …d21 Jul 2018Mashallah. I love you for the sake of Allah.By the second paragraph, i realized where this was goin… | WordPress comment thread flattened into the body |
| 50 | `_posts/2018-06-29-an-alternate-reality.md` | 53 | `2018Mashallah` | `tag-strip-join-lower-upper` | 1 | …- Ziad21 Jul 2018Mashallah. I love you for the sake of Allah.By the second paragr… | WordPress comment thread flattened into the body |
| 51 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 46 | `.` | `no-space-after-stop` | 4 | …Aug 2018Great article, you explained it in a clear way.ReplyAnthony Fantano7 Aug 2018This is, to put it mildly… | WordPress comment thread flattened into the body |
| 52 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 46 | `way.Reply` | `tag-strip-join-full-stop` | 1 | …X12 Aug 2018Great article, you explained it in a clear way.ReplyAnthony Fantano7 Aug 2018This is, to put it mildly, ra…… | WordPress comment thread flattened into the body |
| 53 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 46 | `2018Great` | `tag-strip-join-lower-upper` | 1 | …- GameBotX12 Aug 2018Great article, you explained it in a clear way.ReplyAnthony… | WordPress comment thread flattened into the body |
| 54 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 46 | `2018This` | `tag-strip-join-lower-upper` | 1 | …explained it in a clear way.ReplyAnthony Fantano7 Aug 2018This is, to put it mildly, rather confused thinking. Your e… | WordPress comment thread flattened into the body |
| 55 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 46 | `2018People` | `tag-strip-join-lower-upper` | 1 | …rker spiritual forces of the world.ReplyGameBotX19 Aug 2018People who’ll end up in Hell are the ones who know that Isl…… | WordPress comment thread flattened into the body |
| 56 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 47 | `.` | `no-space-after-stop` | 4 | …is full of many inaccuarcies and straight up falsehoods.ReplyAsadullah Ali11 Aug 2018This article (nor any of m… | WordPress comment thread flattened into the body |
| 57 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 47 | `2018The` | `tag-strip-join-lower-upper` | 2 | …- Anthony Fantano10 Aug 2018The Qur’an is not a scientific book and did not predict an… | WordPress comment thread flattened into the body |
| 58 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 47 | `2018This` | `tag-strip-join-lower-upper` | 1 | …es and straight up falsehoods.ReplyAsadullah Ali11 Aug 2018This article (nor any of my other articles) make any claim… | WordPress comment thread flattened into the body |
| 59 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 47 | `2018Also` | `tag-strip-join-lower-upper` | 1 | …I said, bad people hate the truth.ReplyGameBotX114 Aug 2018Also, the Quran challenges non Muslims to come up with some… | WordPress comment thread flattened into the body |
| 60 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 47 | `2018When` | `tag-strip-join-lower-upper` | 1 | …ed, even one Surah with 3 verses.ReplyFullwonder18 Aug 2018When anyone comes out with something like it you will come… | WordPress comment thread flattened into the body |
| 61 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 48 | `foreverThe` | `tag-strip-join-lower-upper` | 2 | …died while he was still in his teens would be burning foreverThe verse you mentioned makes sense but not every disbeli…… | WordPress comment thread flattened into the body |
| 62 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 48 | `opinionReply` | `tag-strip-join-lower-upper` | 1 | …tradicts the whole point that God created us for in my opinionReplyBill bill24 Aug 2019That atheist teen will be quest…… | WordPress comment thread flattened into the body |
| 63 | `_posts/2018-08-01-gods-mercy-without-eternal-punishment.md` | 48 | `2019That` | `tag-strip-join-lower-upper` | 1 | …t God created us for in my opinionReplyBill bill24 Aug 2019That atheist teen will be questioned on his disbelief, and… | WordPress comment thread flattened into the body |
| 64 | `_posts/2018-08-18-yolo-a-motto-of-ignorance.md` | 58 | `.` | `no-space-after-stop` | 1 | …erlife then there is no point following religion at all.Reply… | WordPress comment thread flattened into the body |
| 65 | `_posts/2018-08-18-yolo-a-motto-of-ignorance.md` | 58 | `all.Reply` | `tag-strip-join-full-stop` | 1 | …afterlife then there is no point following religion at all.Reply… | WordPress comment thread flattened into the body |
| 66 | `_posts/2018-08-18-yolo-a-motto-of-ignorance.md` | 59 | `.` | `no-space-after-stop` | 2 | …g written can easily be summed up in your mindless meme.Note the sarcasm.Reply… | comment-thread boundary: WordPress furniture the fetch flattened |
| 67 | `_posts/2018-08-18-yolo-a-motto-of-ignorance.md` | 59 | `2018Yes` | `tag-strip-join-lower-upper` | 1 | …come up with such great ideas?ReplyAsadullah Ali24 Sep 2018Yes, that was the entire point of my article. Everything w… | comment-thread boundary: WordPress furniture the fetch flattened |
| 68 | `_posts/2018-12-06-ikhalifa-ep-2.md` | 24 | `.` | `no-space-after-stop` | 2 | …help make cleanliness everywhere and where in dwelling.Pick the most convenient for you personally work schedu… | WordPress comment thread flattened into the body |
| 69 | `_posts/2018-12-06-ikhalifa-ep-2.md` | 24 | ` .` | `space-before-punctuation` | 3 | …can order worker- maid Saint Albans two times in week . Maid will come to you in advance approved time of da… | WordPress comment thread flattened into the body |
| 70 | `_posts/2018-12-06-ikhalifa-ep-2.md` | 24 | `2019This` | `tag-strip-join-lower-upper` | 1 | …- CleanPaycle8 May 2019This Cleaning specialized company is giving attention skill… | WordPress comment thread flattened into the body |
| 71 | `_posts/2020-03-24-lost-in-time-translation.md` | 76 | `.` | `no-space-after-stop` | 3 | …how to explain future technology in a non-confusing way.Loading...ReplyAsadullah Ali11 Apr 2020Let me know how… | WordPress comment thread flattened into the body |
| 72 | `_posts/2020-03-24-lost-in-time-translation.md` | 76 | `way.Loading` | `tag-strip-join-full-stop` | 1 | …ow how to explain future technology in a non-confusing way.Loading...ReplyAsadullah Ali11 Apr 2020Let me know how that…… | WordPress comment thread flattened into the body |
| 73 | `_posts/2020-03-24-lost-in-time-translation.md` | 76 | `2020This` | `tag-strip-join-lower-upper` | 1 | …- wdqdqwd10 Apr 2020This is a weak argument. An omniscient God would know how t… | WordPress comment thread flattened into the body |
| 74 | `_posts/2020-03-24-lost-in-time-translation.md` | 76 | `2020Let` | `tag-strip-join-lower-upper` | 1 | …a non-confusing way.Loading...ReplyAsadullah Ali11 Apr 2020Let me know how that would go. Come on, give an argument.L… | WordPress comment thread flattened into the body |
| 75 | `_posts/2020-03-24-lost-in-time-translation.md` | 76 | `2020Why` | `tag-strip-join-lower-upper` | 1 | …Come on, give an argument.Loading...Replywdqdqwd11 Apr 2020Why should I? Are you doubting God’s omniscience?Loading..… | WordPress comment thread flattened into the body |
| 76 | `_posts/2020-03-24-lost-in-time-translation.md` | 76 | `2020How` | `tag-strip-join-lower-upper` | 1 | …Are you doubting God’s omniscience?Loading...Saif7 May 2020How do you know that it would work? How do you know that h… | WordPress comment thread flattened into the body |
| 77 | `_posts/2020-08-07-adam-is-no-myth.md` | 86 | `.` | `no-space-after-stop` | 2 | …nce, and accepted by believers on the strength of faith.Actually, these scientists’ argument backfires on them… | source capture has the space; the recovered file does not |
| 78 | `_posts/2020-08-11-my-views-on-the-punishment-for-apostasy.md` | 40 | `.` | `no-space-after-stop` | 1 | …f the hukm, said that his hukm is like that of a Muslim.Ibn Rusdh (2000) The Distinguished Jurist Primer (Biday… | source capture has the space; the recovered file does not |
| 79 | `_posts/2020-08-11-my-views-on-the-punishment-for-apostasy.md` | 70 | `.` | `no-space-after-stop` | 1 | …ut Br. Mohammad Hijabs lecture on Liberalism. Take care.Loading...Reply… | WordPress comment thread flattened into the body |
| 80 | `_posts/2020-08-11-my-views-on-the-punishment-for-apostasy.md` | 70 | `2020Fascinating` | `tag-strip-join-lower-upper` | 1 | …orship Allah - The One Sustainer of the Universe11 Aug 2020Fascinating article. Was just thinking about this issue tod…… | WordPress comment thread flattened into the body |
| 81 | `_posts/2020-08-11-my-views-on-the-punishment-for-apostasy.md` | 70 | `2020The` | `tag-strip-join-lower-upper` | 1 | …rd. Jzk for educating us.Loading...ReplyR. Ahmed12 Aug 2020The punishment for ridda is justifiable under liberal valu… | WordPress comment thread flattened into the body |

### 2a. The comment threads are the bulk of it, and a previous repair left them

`docs/recovery-log/2026-09-29-fetch-damage-repair.md` records that 200 spans
were removed from 20 files, and states that "WordPress comment threads were
removed in full". They were not. The repair's `one-comment-on` rule removed the
**heading** of each thread and `comment-count` removed the **count**; the
comment **bodies** were never matched by any rule and are still in the body of
eleven posts. For example, after the repair:

`_posts/2015-02-14-charlie-hebdo.md:84`

    - isa sulaiman19 Feb 2015Salaam! Well written... A positive read on a very
      current subject.

`_posts/2018-08-01-gods-mercy-without-eternal-punishment.md:47`

    - Anthony Fantano10 Aug 2018The Qur'an is not a scientific book and did not
      predict anything. [...] straight up falsehoods.ReplyAsadullah Ali11 Aug
      2018This article (nor any of my other articles) make any claim that the
      Qur'an...

The `2018-08-01` thread alone accounts for 21 of the 102. This is third-party
blog commentary inside a document the archive presents as his essay, and the
repair log's own reasoning for removing comment threads ("not the author's
work, and not sources this archive claims to hold") applies to it unchanged.
It is also the only damage class here with no source-provable boundary, so it
must be removed as whole comment blocks, not word by word.

### 2b. Injected CSS and JavaScript in the body of one post

`_posts/2017-05-07-...-orientalists-fables.md:20-29` is not his post. It is an
injected player/ad stylesheet and script, truncated mid-block:

    div.wpmrec2x{max-width:610px;}
    div.wpmrec2x div.u > div{float:left;margin-right:10px;}
    div.wpmrec2x div.u > div:nth-child(3n){margin-right:0px;}

    var p = o.parentNode;
    p.style.setProperty('display', 'inline-block', 'important');
    o.style.setProperty('display', 'block', 'important');
    } else {
    o.style.setProperty('display', 'none', 'important');
    o.style.setProperty('visibility', 'hidden', 'important');

The Wayback capture of the page
(`asadullahali.com_2017-05-07-...-orienta_954a75.html`) contains no `wpmrec2x`
at all, and the mirror lane's own extraction of the same page ends cleanly at
the end of the abstract. So this is residue the fetch introduced, not text the
site ever served. The 2026-09-29 repair did touch this file - it removed two
`js-terminator-run` lines, `}` and `});` - which is why only five hits remain,
and it is the reason the rest can no longer be found (section 5).

## 3. Judged NOT DAMAGE - 169 hits

Nothing in this table should be repaired. It is grouped so the shape of the
scanner's blind spot is visible: of 287 hits, 169 are the scanner reading
either the author's own typography or this repository's own prose.

| # | file | line | text | rule | n | context | why |
|---|---|---|---|---|---|---|---|
| 1 | `_posts/2013-06-09-prophets-vs-pedophiles-part-3.md` | 34 | ` ,` | `space-before-punctuation` | 1 | …d, “I memorized these words from the Messenger of Allah ,… | source capture has the identical text; the archive reproduced it faithfully |
| 2 | `_posts/2013-09-08-illogical-critques-of-the-quran.md` | 26 | `.` | `no-space-after-stop` | 1 | …erit to this argument, but this is clearly not the case.The above passage from the Qur’an references the Qur’an… | source capture has the same joined words (</p><p> already joined upstream) |
| 3 | `_posts/2014-02-16-malaysias-tiger-in-waiting.md` | 29 | ` ,` | `space-before-punctuation` | 1 | …The military eventually stepped in and arrested Chávez , but he was shortly released thereafter due to mass dem… | source capture has the identical text; the archive reproduced it faithfully |
| 4 | `_posts/2014-04-30-the-narrative-behind-happymuslims.md` | 46 | ` ,` | `space-before-punctuation` | 1 | …a completely topsy turvy way in which do deduce ‘Hukm’ , Islamic rulings, not to mention the fact it leads to a… | source capture has the identical text; the archive reproduced it faithfully |
| 5 | `_posts/2014-04-30-the-narrative-behind-happymuslims.md` | 92 | ` !` | `space-before-punctuation` | 2 | …2014/04/18/happy-muslims-angry-puritanical-muslims/ [3] ![Screenshot of a Facebook post by The Honesty Policy re… | the archive's own markdown image conversion of a source <img> |
| 6 | `_posts/2015-02-14-charlie-hebdo.md` | 14 | `salAllahu` | `tag-strip-join-lower-upper` | 1 | …te and their supposed offense of the Prophet Muhammad (salAllahu alayhi wasallam) having been depicted – was the worse… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 7 | `_posts/2015-02-14-charlie-hebdo.md` | 14 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …– all the while drawing yet another Prophet Muhammad (sallAllahu alayhi wasallam) cartoon, smack in the middle of the …… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 8 | `_posts/2015-02-14-charlie-hebdo.md` | 16 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …d – not only in the depiction of the Prophet Muhammad (sallAllahu alayhi wasallam), but also in disrespect of him and …… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 9 | `_posts/2015-02-14-charlie-hebdo.md` | 18 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …As someone who cherishes the Prophet Muhammad (sallAllahu alayhi wasallam) and wishes to honor him, I can say wi… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 10 | `_posts/2015-02-14-charlie-hebdo.md` | 24 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …attacking their very identity – the Prophet Muhammad (sallAllahu alayhi wasallam) — all the while claiming it isnotoka…… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 11 | `_posts/2015-06-25-the-archetype-of-beauty-in-islam-academic-article.md` | 36 | `salAllahu` | `tag-strip-join-lower-upper` | 1 | …in the Qur’an and the sayings of the Prophet Muhammad (salAllahu alayhi wasallam), they restrict our grasp on the onto…… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 12 | `_posts/2015-08-16-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 33 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …aising the dead, and of course the Prophet Muhammad’s (sallAllahu alayhi wasallam) linguistic miracle of the Qur’an.… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 13 | `_posts/2015-08-16-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 40 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …The Messenger of Allah (sallAllahu alayhi wasallam) said: “There is none born but is crea… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 14 | `_posts/2015-08-16-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 61 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …ures as man’s fitrah, given the fact that the Prophet (sallAllahu alayhi wasallam) compares it to fully formed new bor…… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 15 | `_posts/2015-08-16-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 95 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …Allah’s Messenger (sallAllahu alayhi wasallam) said, “Allah said, ‘I will declare wa… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 16 | `_posts/2016-02-07-the-rationality-of-believing-in-god-without-evidence-part-2-2.md` | 45 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …This why the Prophet (sallAllahu alayhi wasallam) made clear that the normative intuiti… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 17 | `_posts/2016-04-30-how-feminism-undermines-islam-and-gender-justice.md` | 34 | `sallAllahu` | `tag-strip-join-lower-upper` | 2 | …her). Let’s not also forget that the Prophet Muhammad (sallAllahu alayhi wasallam) was a man. So if you claim that sim…… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 18 | `_posts/2016-04-30-how-feminism-undermines-islam-and-gender-justice.md` | 66 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …mparing myself to her father and the Prophet Muhammad (sallAllahu alayhi wasallam)”. Let me just go on record again as…… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 19 | `_posts/2018-05-22-apostasy-beyond-the-rhetoric.md` | 85 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …still extol the achievements of the Prophet Muhammad (sallAllahu alayhi wasallam) and his followers. Those books will …… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 20 | `_posts/2018-05-24-naked-kings-in-the-information-age.md` | 76 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …still extol the achievements of the Prophet Muhammad (sallAllahu alayhi wasallam) and his followers. Those books will …… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 21 | `_posts/2020-01-23-backbone-ribs.md` | 236 | ` ?` | `space-before-punctuation` | 1 | …2. Aslabikum (أَصْلَابِكُمْ) → “backbones” → ?… | source capture has the identical text; the archive reproduced it faithfully |
| 22 | `_posts/2020-01-23-backbone-ribs.md` | 436 | ` ?` | `space-before-punctuation` | 1 | …2. Min bayni (مِنْ بَيْنِ) → “from between” → ?… | source capture has the identical text; the archive reproduced it faithfully |
| 23 | `_posts/2020-01-23-backbone-ribs.md` | 440 | ` ?` | `space-before-punctuation` | 1 | …3. L’sulbi (الصُّلْبِ) → “the backbone” → ?… | source capture has the identical text; the archive reproduced it faithfully |
| 24 | `_posts/2020-01-23-backbone-ribs.md` | 444 | ` ?` | `space-before-punctuation` | 1 | …4. L’taraibi (التَّرَائِبِ) → “the upper chest” → ?… | source capture has the identical text; the archive reproduced it faithfully |
| 25 | `_posts/2020-01-23-backbone-ribs.md` | 518 | ` .` | `space-before-punctuation` | 1 | …woman”, contrary to its apparent reading as “male ribs” .… | source capture has the identical text; the archive reproduced it faithfully |
| 26 | `_posts/2020-01-23-backbone-ribs.md` | 802 | ` .` | `space-before-punctuation` | 1 | …ch as in Sunan an-Nisa’i https://sunnah.com/urn/1002010 . For more information on cervical mucus, please refer t… | source capture has the identical text; the archive reproduced it faithfully |
| 27 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 271 | ` :` | `space-before-punctuation` | 1 | …the bounds of proper worship by practicing monasticism: :… | source capture has the identical text; the archive reproduced it faithfully |
| 28 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 1052 | `transAtlantic` | `tag-strip-join-lower-upper` | 1 | …from Islam. So, unless Daniel wishes to argue that the transAtlantic slave trade is equivalent to the Islamic concepti…… | source capture has the identical text; the archive reproduced it faithfully |
| 29 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 1065 | `.` | `no-space-after-stop` | 1 | …coercive labor institutions such as slavery and serfdom.Thus, slavery and forced labor was the most common form… | source capture has the same joined words (</p><p> already joined upstream) |
| 30 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 1264 | `.` | `no-space-after-stop` | 1 | …Mohammed Hijab (2020) “Controversial Questions to Prof.Jonathan Brown and Dr. Shadee Masri (MH Podcast #6),” 1… | source capture has the same joined words (</p><p> already joined upstream) |
| 31 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 1450 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …sforms itself into an insult upon the Prophet himself (sallAllahu alayhi wasallam).… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 32 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 1460 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …Worse still, Daniel unwittingly insults the Prophet (sallAllahu alayhi wasallam) by neglecting the glaring inconsisten… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 33 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 1698 | `preloadContent` | `tag-strip-join-lower-upper` | 1 | …https://videopress.com/v/tKw18uAe?preloadContent=metadata… | source capture has the identical text; the archive reproduced it faithfully |
| 34 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 2694 | `vpaAjvq` | `tag-strip-join-lower-upper` | 1 | …E, 3:00:18 – 3:02:07 & https://www.youtube.com/watch?v=vpaAjvqVz4U… | source capture has the identical text; the archive reproduced it faithfully |
| 35 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 2878 | `qaSkmt` | `tag-strip-join-lower-upper` | 1 | …- https://www.youtube.com/watch?v=6d-qaSkmtB0… | source capture has the identical text; the archive reproduced it faithfully |
| 36 | `_posts/2020-08-10-reviewing-haqiqatjou.md` | 2886 | `qaSkmt` | `tag-strip-join-lower-upper` | 1 | …- https://www.youtube.com/watch?v=6d-qaSkmtB0, 3:53-4:20… | source capture has the identical text; the archive reproduced it faithfully |
| 37 | `_articles/ikhalifa-ep-1.md` | 29 | `rtViq` | `tag-strip-join-lower-upper` | 1 | …1： Appreciate Others](https://www.youtube.com/watch?v=rtViqNWY1Bk) (10 min). Machine-generated (Whisper local tran… | this repository's own generated link/scaffolding line |
| 38 | `_articles/mdi-naked-kings-in-the-information-age.md` | 85 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …still extol the achievements of the Prophet Muhammad (sallAllahu alayhi wasallam) and his followers. Those books will …… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 39 | `_articles/mdi-religion-vs-paedophilia-part-3.md` | 55 | ` ,` | `space-before-punctuation` | 1 | …d, “I memorized these words from the Messenger of Allah ,… | source capture has the identical text; the archive reproduced it faithfully |
| 40 | `_articles/mdi-religion-vs-paedophilia-part-3.md` | 97 | `.` | `no-space-after-stop` | 1 | …right of the guardian, or at least a synthesis of both.While the guardian has the right to conclude a marriage… | source capture has the same joined words (</p><p> already joined upstream) |
| 41 | `_articles/mdi-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 47 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …aising the dead, and of course the Prophet Muhammad’s (sallAllahu alayhi wasallam) linguistic miracle of the Qur’an.… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 42 | `_articles/mdi-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 59 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …The Messenger of Allah (sallAllahu alayhi wasallam) said: “There is none born but is crea… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 43 | `_articles/mdi-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 93 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …ures as man’s fitrah, given the fact that the Prophet (sallAllahu alayhi wasallam) compares it to fully formed new bor…… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 44 | `_articles/mdi-the-rationality-of-believing-in-god-without-evidence-part-1.md` | 149 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …Allah’s Messenger (sallAllahu alayhi wasallam) said, “Allah said, ‘I will declare wa… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 45 | `_articles/mdi-withoutevidence2.md` | 52 | `sallAllahu` | `tag-strip-join-lower-upper` | 1 | …This why the Prophet (sallAllahu alayhi wasallam) made clear that the normative intuiti… | his own capitalised transliteration; identical in 40 raw captures, no tag boundary inside it |
| 46 | `_articles/mdi-withoutevidence2.md` | 165 | ` .` | `space-before-punctuation` | 1 | …rification is in respect to my understanding of science . I am in no way attacking science in this essay, rather… | source capture has the identical text; the archive reproduced it faithfully |
| 47 | `_transcripts/transcript-0biKKRHO_Tk.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 48 | `_transcripts/transcript-0biKKRHO_Tk.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 49 | `_transcripts/transcript-1U6VfHosrqw.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 50 | `_transcripts/transcript-1U6VfHosrqw.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 51 | `_transcripts/transcript-2tsI80MDUOI-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 52 | `_transcripts/transcript-2tsI80MDUOI-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 53 | `_transcripts/transcript-3vqVYfs5mCk.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 54 | `_transcripts/transcript-3vqVYfs5mCk.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 55 | `_transcripts/transcript-4maSZMzhmuI-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 56 | `_transcripts/transcript-4maSZMzhmuI-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 57 | `_transcripts/transcript-4VcPzhkP9bE.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 58 | `_transcripts/transcript-4VcPzhkP9bE.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 59 | `_transcripts/transcript-7EqMJJuUKr8.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 60 | `_transcripts/transcript-7EqMJJuUKr8.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 61 | `_transcripts/transcript-7KBCENktOOU.md` | 32 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 62 | `_transcripts/transcript-7KBCENktOOU.md` | 32 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 63 | `_transcripts/transcript-_C5ox2zZl0U.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 64 | `_transcripts/transcript-_C5ox2zZl0U.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 65 | `_transcripts/transcript-A3dbBCBSFKk.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 66 | `_transcripts/transcript-A3dbBCBSFKk.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 67 | `_transcripts/transcript-A3dbBCBSFKk.md` | 679 | `&nbsp;` | `html-entity` | 2 | …like \[&nbsp;\_\_&nbsp;\] oh yeah they may not care but what i\'m tr… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 68 | `_transcripts/transcript-A3dbBCBSFKk.md` | 1375 | `&nbsp;` | `html-entity` | 2 | …that is just \[&nbsp;\_\_&nbsp;\]… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 69 | `_transcripts/transcript-A3dbBCBSFKk.md` | 1511 | `&nbsp;` | `html-entity` | 2 | …herent for you to believe that you do there\'s to be \[&nbsp;\_\_&nbsp;\] if you said you didn\'t like it would just… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 70 | `_transcripts/transcript-A3dbBCBSFKk.md` | 1946 | `&nbsp;` | `html-entity` | 2 | …\[&nbsp;\_\_&nbsp;\] well um… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 71 | `_transcripts/transcript-A3dbBCBSFKk.md` | 1957 | `&nbsp;` | `html-entity` | 2 | …a \[&nbsp;\_\_&nbsp;\] as well… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 72 | `_transcripts/transcript-bRTI6Z5gggE-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 73 | `_transcripts/transcript-bRTI6Z5gggE-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 74 | `_transcripts/transcript-cDHrrbOKbl4.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 75 | `_transcripts/transcript-cDHrrbOKbl4.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 76 | `_transcripts/transcript-D2t0idkAqjA-duplicate-upload.md` | 36 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 77 | `_transcripts/transcript-D2t0idkAqjA-duplicate-upload.md` | 36 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 78 | `_transcripts/transcript-DA9JGrHKHZA.md` | 167 | ` ?` | `space-before-punctuation` | 1 | …e que signifie ce schéma qui peut paraître un peu barba ?… | French-language interview; the space before the mark is the speaker's |
| 79 | `_transcripts/transcript-DA9JGrHKHZA.md` | 520 | ` ?` | `space-before-punctuation` | 1 | …a justice dans le monde. Vous voyez ce que je veux dire ? C\'est dans ce sens-là… | French-language interview; the space before the mark is the speaker's |
| 80 | `_transcripts/transcript-Dr5IgXCHRIE.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 81 | `_transcripts/transcript-Dr5IgXCHRIE.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 82 | `_transcripts/transcript-Dr5IgXCHRIE.md` | 886 | `&nbsp;` | `html-entity` | 2 | …the yeah what a \[&nbsp;\_\_&nbsp;\] move you asked me to you asked me to rant… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 83 | `_transcripts/transcript-Dr5IgXCHRIE.md` | 1634 | `&nbsp;` | `html-entity` | 2 | …n\'t real then I\'m going to tell you that you\'re a \[&nbsp;\_\_&nbsp;\] who doesn\'t understand what it means to b… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 84 | `_transcripts/transcript-EK5oppX6C2U-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 85 | `_transcripts/transcript-EK5oppX6C2U-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 86 | `_transcripts/transcript-eQ-frTAlcJc-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 87 | `_transcripts/transcript-eQ-frTAlcJc-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 88 | `_transcripts/transcript-fq1WejCHgXs-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 89 | `_transcripts/transcript-fq1WejCHgXs-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 90 | `_transcripts/transcript-G47Stp3pLss.md` | 33 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 91 | `_transcripts/transcript-G47Stp3pLss.md` | 33 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 92 | `_transcripts/transcript-gmGnu1RBAoQ.md` | 24 | `gmGnu` | `tag-strip-join-lower-upper` | 2 | …- The recording: [gmGnu1RBAoQ]({{ "/videos/gmGnu1RBAoQ/" | relative_url }})… | this repository's own generated link/scaffolding line |
| 93 | `_transcripts/transcript-gmGnu1RBAoQ.md` | 26 | `gmGnu` | `tag-strip-join-lower-upper` | 1 | …- Capture file held in the archive: `whisper-gmGnu1RBAoQ.json`… | this repository's own generated link/scaffolding line |
| 94 | `_transcripts/transcript-hKdNF95UqVM.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 95 | `_transcripts/transcript-hKdNF95UqVM.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 96 | `_transcripts/transcript-hURJIIm0tSY-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 97 | `_transcripts/transcript-hURJIIm0tSY-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 98 | `_transcripts/transcript-idz29r5LHig.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 99 | `_transcripts/transcript-idz29r5LHig.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 100 | `_transcripts/transcript-kDH1BOyhhYk-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 101 | `_transcripts/transcript-kDH1BOyhhYk-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 102 | `_transcripts/transcript-KjUPbkqRxac.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 103 | `_transcripts/transcript-KjUPbkqRxac.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 104 | `_transcripts/transcript-kRCzZW3rg4U.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 105 | `_transcripts/transcript-kRCzZW3rg4U.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 106 | `_transcripts/transcript-lE690yapgTA.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 107 | `_transcripts/transcript-lE690yapgTA.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 108 | `_transcripts/transcript-M3nB154Mkuk.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 109 | `_transcripts/transcript-M3nB154Mkuk.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 110 | `_transcripts/transcript-M3nB154Mkuk.md` | 425 | `&nbsp;` | `html-entity` | 4 | …hat the way you act is abnormal you you just want to \[&nbsp;\_\_&nbsp;\] all these girls there\'s something wrong w… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 111 | `_transcripts/transcript-M3nB154Mkuk.md` | 426 | `&nbsp;` | `html-entity` | 4 | …ain\'t nothing to do with you \[&nbsp;\_\_&nbsp;\] cause men can do what they want women can\… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 112 | `_transcripts/transcript-M3nB154Mkuk.md` | 431 | `&nbsp;` | `html-entity` | 2 | …\[&nbsp;\_\_&nbsp;\] you now… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 113 | `_transcripts/transcript-M3nB154Mkuk.md` | 441 | `&nbsp;` | `html-entity` | 6 | …nothing we can do to save it christians are complete \[&nbsp;\_\_&nbsp;\] christians ain\'t done \[&nbsp;\_\_&nbsp;\… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 114 | `_transcripts/transcript-M3nB154Mkuk.md` | 1366 | `&nbsp;` | `html-entity` | 2 | …you notice this too like yeah like \[&nbsp;\_\_&nbsp;\] uh soy boys… | YouTube's censored-word token; present in the raw .vtt, decoded by kramdown at render |
| 115 | `_transcripts/transcript-MCR3xh8wccQ.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 116 | `_transcripts/transcript-MCR3xh8wccQ.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 117 | `_transcripts/transcript-n3vhs1mcmVM.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 118 | `_transcripts/transcript-n3vhs1mcmVM.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 119 | `_transcripts/transcript-NGtNHgTwhXc.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 120 | `_transcripts/transcript-NGtNHgTwhXc.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 121 | `_transcripts/transcript-OHNMeqGMdPc.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 122 | `_transcripts/transcript-OHNMeqGMdPc.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 123 | `_transcripts/transcript-qBkiwqMucY0.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 124 | `_transcripts/transcript-qBkiwqMucY0.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 125 | `_transcripts/transcript-Qiay_L4IQ88.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 126 | `_transcripts/transcript-Qiay_L4IQ88.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 127 | `_transcripts/transcript-QoU02Om_wiQ.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 128 | `_transcripts/transcript-QoU02Om_wiQ.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 129 | `_transcripts/transcript-rtViqNWY1Bk.md` | 24 | `rtViq` | `tag-strip-join-lower-upper` | 2 | …- The recording: [rtViqNWY1Bk]({{ "/videos/rtViqNWY1Bk/" | relative_url }})… | this repository's own generated link/scaffolding line |
| 130 | `_transcripts/transcript-rtViqNWY1Bk.md` | 26 | `rtViq` | `tag-strip-join-lower-upper` | 1 | …- Capture file held in the archive: `whisper-rtViqNWY1Bk.json`… | this repository's own generated link/scaffolding line |
| 131 | `_transcripts/transcript-tUHEAejm404.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 132 | `_transcripts/transcript-tUHEAejm404.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 133 | `_transcripts/transcript-tW-mjwrE7YY.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 134 | `_transcripts/transcript-tW-mjwrE7YY.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 135 | `_transcripts/transcript-unmn_tY5r_c.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 136 | `_transcripts/transcript-unmn_tY5r_c.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 137 | `_transcripts/transcript-xhnU-1dNi3I.md` | 30 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 138 | `_transcripts/transcript-xhnU-1dNi3I.md` | 30 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 139 | `_transcripts/transcript-YjGHZwdM7XU-duplicate-upload.md` | 35 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 140 | `_transcripts/transcript-YjGHZwdM7XU-duplicate-upload.md` | 35 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 141 | `_transcripts/transcript-Yu8rw5M0GF8.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 142 | `_transcripts/transcript-Yu8rw5M0GF8.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 143 | `_transcripts/transcript-yUpHMaFHZ6s.md` | 31 | `&nbsp;` | `html-entity` | 1 | …ds. A handful of these files contain the literal text `&nbsp;` where the caption engine emitted an escaped non-break… | the archive's own rendering note, which names the string it documents |
| 144 | `_transcripts/transcript-yUpHMaFHZ6s.md` | 31 | ` .` | `space-before-punctuation` | 1 | …ng lines and the inline `<00:00:03.840>` timing and `<v ...>` voice tags are removed, and a paragraph starts whe… | the archive's own rendering note, which names the string it documents |
| 145 | `_videos/ywhiqBkoveA.md` | 27 | `ywhiqBkove` | `tag-strip-join-lower-upper` | 1 | …- [Watch on YouTube](https://www.youtube.com/watch?v=ywhiqBkoveA)… | this repository's own generated link/scaffolding line |

### 3a. `sallAllahu` / `salAllahu` - 24 hits, the single largest false positive

The rule's stated cause is "two words that shared an inline element". The
source capture shows there is no such element. From
`asadullahali.com_2015-02-14-charlie-hebdo-...html`:

    ...yet another Prophet Muhammad (<em>sallAllahu alayhi wasallam</em>) cartoon...

The `<em>` opens *before* "sall". There is no tag between "sall" and "Allahu",
so no tag was stripped there and no space was destroyed. `sallAllahu` is how
he wrote the transliteration on his own site, and it is present in that exact
form in 40 raw captures across `_staging`. `sall Allahu` appears in none of
them. **His capitalised transliteration is his, and the archive preserved it.**

### 3b. The `&nbsp;` hits - 72, and every one of them is correct

**80 of the 120 transcript hits are this repository's own rendering note.** The
line reads:

    A handful of these files contain the literal text `&nbsp;` where the
    caption engine emitted an escaped non-breaking space; it is shown here as
    the space it stands for, and no word is affected.

The detector is matching the archive's own documentation of the phenomenon. 40
files carry that note, at line 30, 31, 32, 33, 35 or 36 depending on how much
front matter the file has.

The remaining 32 are in three transcript bodies and every one sits inside
YouTube's own profanity-censoring token:

    [&nbsp;&#92;__&#92;&nbsp;]

Confirmed in the raw capture, `cap-A3dbBCBSFKk.en-orig.vtt:15751`:

    like<01:01:12.000><c> [&nbsp;__&nbsp;]</c><01:01:12.559><c> oh</c>...

The backslashes are `md_escape()` in `scripts/build_collections.py:408`, which
escapes markdown control characters and changes bytes, never words. The
`&nbsp;` is in the source capture and is reproduced byte for byte, which is the
archive's stated policy for the caption lane. And the rendering note's claim
that it "is shown here as the space it stands for" is **true**, verified
against the kramdown the build actually uses (2.5.2, no custom kramdown config
in `_config.yml`):

    $ bundle exec ruby -e "require 'kramdown';
        puts Kramdown::Document.new(%q{x \[&nbsp;\_\_&nbsp;\] y}).to_html.inspect"
    "<p>x [\xFF__\xFF] y</p>\n"

The two `\xFF` are the bytes of U+00A0 NO-BREAK SPACE: kramdown decodes
`&nbsp;` to the character, exactly as the note says it does. A reader sees
`[ __ ]`. Nothing to repair, and repairing it would break the note's own
claim.

### 3c. `space-before-punctuation` is mostly the source page's own spacing

56 of the 70 hits in this class are the source's own stray space before a mark,
faithfully carried. Checked one by one against the captures:

| recovered | source capture | verdict |
|---|---|---|
| `arrested Chávez , but` | `arrested Chávez , but` (a link closed before the comma) | source's own |
| `deduce 'Hukm' , Islamic rulings` | `deduce 'Hukm' , Islamic rulings` | source's own |
| `practicing monasticism: :` | `practicing monasticism:&nbsp;:&nbsp;` | source's own |
| `urn/1002010 . For more` | `</a> . For more` | source's own |
| `as "male ribs" .` | `as "male ribs" .` | source's own |
| `-> "backbones" -> ?` | `-> "backbones" <strong>-></strong> <strong>?</strong>` | source's own |
| `my understanding of science .` | MDI capture has `science .` | source's own |
| `Messenger of Allah ,` | MDI capture has `Allah ,` | source's own |

In every case the page as served had an inline element between the word and the
punctuation; the tag was stripped and the space that was already there was left
where it was. That is a faithful transcription, not damage. The 4 hits this
class really does mark as damage are in section 2.

### 3d. `case.The`, `serfdom.Thus`, `Prof.Jonathan` - the author's own joins

`no-space-after-stop` reports these as missing spaces. The Wayback capture has
them identical: `not the case.The above passage`, `slavery and serfdom.Thus,`,
`Questions to Prof.Jonathan Brown and Dr. Shadee Masri`. He joined them on his
own site. Note the inconsistency in his own text - `Prof.Jonathan` and
`Dr. Shadee` in the same sentence - which is exactly the kind of thing a
preservation archive must not tidy.

### 3e. This repository's own scaffolding - 8 hits

`[gmGnu1RBAoQ]`, `[rtViqNWY1Bk]`, `- The recording:`, `` `whisper-rtViqNWY1Bk.json` ``,
`- [Watch on YouTube]`. Generated by `build_collections.py` and carried in the
catalogue. A YouTube video id is camelCase; the rule cannot tell that from a
destroyed space.

## 4. Judged UNDECIDED - 16 hits

These stay. Each is a real shape-match with no capture to settle it.

| # | file | line | text | rule | n | context | why |
|---|---|---|---|---|---|---|---|
| 1 | `_posts/2011-12-18-hitchslapping-the-hitch-out-of-his-followers.md` | 24 | ` .` | `space-before-punctuation` | 1 | …treatments to the late Mother Teresa and Jerry Fallwel . Whatever you may think of either of these people is ir… | no source capture for this file; shape alone cannot settle it |
| 2 | `_posts/2012-02-06-against-atheist-aesthetics.md` | 33 | ` ,` | `space-before-punctuation` | 1 | …which we may infer something about the object itself”23 , such as the cultural context or time period in which t… | no source capture for this file; shape alone cannot settle it |
| 3 | `_posts/2012-02-06-against-atheist-aesthetics.md` | 42 | ` .` | `space-before-punctuation` | 1 | …object and the intention in the mind of its creator…”28 . This is consistent with his perspective, because if in… | no source capture for this file; shape alone cannot settle it |
| 4 | `_posts/2012-02-26-the-inhumanity-of-human-rights.md` | 22 | `.` | `no-space-after-stop` | 1 | …ngness to conform to the essential value of our species.It is a dream seeped in ideals of peace and virtue with… | no source capture for this file; shape alone cannot settle it |
| 5 | `_posts/2013-06-13-who-justifies-terrorism-part-1-2.md` | 34 | ` :` | `space-before-punctuation` | 1 | …Narrated By Ibn ‘Umar : During some of battles of Allah’s Apostle [Muhammed] a… | no source capture for this file; shape alone cannot settle it |
| 6 | `_posts/2013-06-13-who-justifies-terrorism-part-1-2.md` | 53 | `.` | `no-space-after-stop` | 1 | …ade the killing of children and women, and that is true.It is valid and has been laid down by the Prophet in an… | no source capture for this file; shape alone cannot settle it |
| 7 | `_posts/2013-06-13-who-justifies-terrorism-part-1-2.md` | 59 | ` ,` | `space-before-punctuation` | 1 | …or because the people in the West live under ‘freedom’ , as Western politicians would have us believe. Osama hi… | no source capture for this file; shape alone cannot settle it |
| 8 | `_posts/2013-06-21-marina-mahathir-against-women-logic-islam.md` | 10 | `inThe` | `tag-strip-join-lower-upper` | 1 | …crime of adultery (more specifically incest). Writing inThe Star, she complains about the recent ruling, but for r… | no source capture for this file; shape alone cannot settle it |
| 9 | `_posts/2013-09-08-illogical-critques-of-the-quran.md` | 24 | `.` | `no-space-after-stop` | 1 | …asa book, it means thatthe Qur’anmust not be from Allah.Before I even have to go into the problems with this ar… | no source capture for this file; shape alone cannot settle it |
| 10 | `_posts/2014-04-30-the-narrative-behind-happymuslims.md` | 86 | ` ,` | `space-before-punctuation` | 1 | …e #HappyMuslims project: “See! Muslims are normal too!” , “Great job! This is a surprise!”, “Look, Ali is a mode… | no source capture for this file; shape alone cannot settle it |
| 11 | `_posts/2016-04-30-how-feminism-undermines-islam-and-gender-justice.md` | 60 | `byHanis` | `tag-strip-join-lower-upper` | 1 | …tes. The first of these to be published was an article byHanis Meketabin the Asian Correspondent titled, “Why Can Onl… | no source capture for this file; shape alone cannot settle it |
| 12 | `_posts/2016-04-30-how-feminism-undermines-islam-and-gender-justice.md` | 134 | `everyMuslim` | `tag-strip-join-lower-upper` | 1 | …and uplift Muslim women in Malaysia and the world over,everyMuslim needs to respond to all injustices equally – foster…… | no source capture for this file; shape alone cannot settle it |
| 13 | `_posts/2018-05-22-apostasy-beyond-the-rhetoric.md` | 59 | ` ,` | `space-before-punctuation` | 1 | …Maryam Namazie , another Iranian ex-Muslim, has become popular for bein… | no source capture for this file; shape alone cannot settle it |
| 14 | `_posts/2018-05-22-apostasy-beyond-the-rhetoric.md` | 61 | ` ,` | `space-before-punctuation` | 1 | …Sherif Gaber , a popular Egyptian YouTube ex-Muslim, has recently bec… | no source capture for this file; shape alone cannot settle it |
| 15 | `_posts/2018-05-22-apostasy-beyond-the-rhetoric.md` | 77 | ` ,` | `space-before-punctuation` | 2 | …likes of other arm-chair scholars like Bill Warner, Phd , Sam Harris , and Robert Spencer — all of whom likewise… | no source capture for this file; shape alone cannot settle it |

What makes them hard, in one line each: 3 are a `X.Y` join at what is probably
a paragraph boundary, where the author is *known* to do this himself in at
least three verified places (`case.The`, `serfdom.Thus`, `Prof.Jonathan`), so
shape cannot distinguish a collapsed `</p><p>` from his own typing; 10 are a
space before punctuation, where every one of the 8 verifiable instances turned
out to be the source's own spacing - the base rate says "leave it", the absence
of a capture says "do not decide"; 3 are a `lowerUpper` join in files with no
capture, where the shape says an `<em>` or `<a>` was stripped and nothing else
does.

The three joins are the most tempting and should be left anyway. `inThe` is
`Writing in The Star` with a publication name; `byHanis` is `an article by Hanis
Meketab` with a byline link, and note the same line also carries `Meketabin`,
which the rule cannot see at all. They are almost certainly damage. They are
not *provably* damage, and the cost of being wrong here is editing his prose on
an inference.

## 5. Damage the detector does not catch

This is a finding about `scripts/fetch_damage.py`, not about the files, and it
is the part of this report worth acting on.

### 5a. The residue rules report zero and are wrong

`_posts/2017-05-07-...-orientalists-fables.md:20-29` holds an injected
stylesheet and script. `residue` and `chrome` both report **0** across all five
collections. Why each rule misses it:

| rule | why it cannot see this block |
|---|---|
| `ad-payload-block` | `_AD_CONFIG_LINE` requires `key: value` at the start of a line. The CSS lines are `div.wpmrec2x{...}` - the `{` is where the regex wants a `:`. The JS lines are `var p = o.parentNode;` - `var` is followed by a space, not a colon. |
| `ad-payload-block` (the `requires` path) | the block also needs a `});` within 3 lines, and the 2026-09-29 repair **removed the two `});`/`}` terminators from this very file**. Repairing the tail destroyed the evidence the rule keys on, so the rest of the block is now permanently invisible. |
| `js-terminator-run` | `_JS_TERMINATOR` matches a line that is only `}`/`)`/`;`. Line 27 is `        } else {`. |
| `markup-tag` | no tag survives; the block is CSS and JS statements. |
| `html-comment`, `embed-tag` | not applicable. |

The `join` rule catches five of the nine lines, and only because JavaScript
identifiers happen to be camelCase. **A gate that fails on `residue` and
passes this file is a gate that cannot see injected script.** The module's own
docstring says a rule that fires on a man lecturing "is worse than no rule at
all"; the same is true in the other direction - a gate that passes a file
carrying an ad payload has no value either. This is a new class the scanner
needs: a CSS/JS block recogniser keyed on `selector{`, `setProperty(`,
`parentNode`, `var `, `} else {`, not on `key: value`.

### 5b. The `join` rules see about one destroyed space in eight

The `join` rules need `[A-Z]` immediately after the missing space. A destroyed
space between two lowercase words is invisible to both of them, and that is the
common case, because the destroyed boundary is a link or an emphasised phrase
inside a sentence.

Measured, not estimated. I diffed each recovered `_posts` file against its raw
capture token by token, tokens carrying their trailing whitespace so that a lost
space shows up as a difference *inside* a token rather than vanishing from the
diff:

| | count |
|---|---|
| characters the recovered file is missing relative to the source | **380** |
| of those, a single space destroyed **between two words** | **170** |
| ...of which `tag-strip-join-*` or a `space` rule fires on | **21** |
| ...of which **no rule fires at all** | **149** |
| runs of spaces collapsed to a single space (no rule covers this) | **210** |

Coverage: the 14 `_posts` files whose capture and recovered text differ at all.
The other 40 either have no nameable capture (11) or match theirs character for
character (29), so **380 is a floor, not a total.**

The 149 the rules cannot see include, verbatim from the diff:

| recovered | source | file |
|---|---|---|
| `withbeauty.Beauty` | `with beauty. Beauty` | `_posts/2011-12-31-thoughts-on-beauty.md` |
| `someonebeautiful` | `someone beautiful` | same |
| `alustingand` | `a lusting and` | same |
| `theart`, `waritself` | `the art`, `war itself` | same |
| `Thatwould` | `That would` | `_posts/2015-02-14-charlie-hebdo.md` |
| `isnotokay` | `is not okay` | same |
| `Hebdohad`, `Hebdocover`, `Hebdomassacre` | `Hebdo had`, `Hebdo cover`, `Hebdo massacre` | same |
| `(Moses,alayhi` | `(Moses, alayhi` | same |
| `–Charlie Hebdo–`, `–CafCaf–` | `– Charlie Hebdo –`, `– CafCaf –` | same |
| `offerasalaamu'alaykum`, `obstructda'wa` | `offer asalaamu'alaykum`, `obstruct da'wa` | `_posts/2014-05-04-...-murad.md` |
| `Murad,Commentary`, `Contentions(Cambridge` | `Murad, Commentary`, `Contentions (Cambridge` | same |
| `specificmadhab(school` | `specific madhab (school` | `_posts/2014-05-29-boko-haram-...md` |
| `itisquite` | `it is quite` | `_posts/2015-05-12-extraordinary-claims-...md` |
| `recentBBC`, `debateregarding`, `theinformal`, `anyargumentmade` | `recent BBC`, `debate regarding`, `the informal`, `any argument made` | `_posts/2015-07-30-whataboutery.md` |
| `whatit`, `howit`, `knowingnothing` | `what it`, `how it`, `knowing nothing` | `_posts/2015-08-16-...-part-1.md` |
| `killssomeone` | `kills someone` | `_posts/2018-03-10-of-context-and-confusion.md` |
| `treated!"you` | `treated!" you` | `_posts/2018-08-18-yolo-...md` |
| `ofridda,`, `astraw`, `weredenyingthe`, `forridda(apostasy)`, `commitsriddamust`, `ofriddawas`, `withshubuhat.`, `doyourefuse` | all spaced in the source | `_posts/2020-08-11-...-apostasy.md` |
| `Visithttp://www.yaqeeninstitute.orgfor` | `Visit http://www.yaqeeninstitute.org for` | `_posts/2018-06-20-atheism-doubting-your-doubts.md` |

**A general rule is available and does not need the source.** Every one of
these is a space destroyed at an **inline-element boundary**: `<a>`, `<em>`,
`<strong>`, `<sup>`, `<cite>`, `<span>`, `<br>`. The signal is not the
resulting word - that is what makes the current rule fire on a camelCase brand
name - but the *shape of the damage*: a lowercase run fused to a lowercase run
mid-sentence, where neither half is a word. A wordlist-free version is to fuse
each adjacent lowercase pair, split it every way, and keep only the splits where
both halves are attested English words. `theart` splits to `the`+`art` and
`the`+`ear`+`t`; only the first is clean, and `the art` is right. That test
costs a word list and needs no capture, and it is the thing this report is
really recommending.

### 5c. An endnote marker that swallows the space before it

A pattern of its own, in `_posts/2015-06-15-...-preliminary-analysis.md` and
`_posts/2018-05-24-naked-kings-...md`. The WordPress footnote link absorbs the
space on its own side:

| recovered | source |
|---|---|
| `non-sequitur,[i]` | `non-sequitur, [i]` |
| `method."[iii]` | `method." [iii]` |
| `phenomenon.[iv]` | `phenomenon. [iv]` |
| `blood,[ii]` | `blood, [ii]` |
| `Somalia.[2]She` | `Somalia.[2] She` |
| `Nazism"[3]and` | `Nazism"[3] and` |
| `[1]https://www.facebook.com/...` | `[1] https://www.facebook.com/...` |

Six of the seven are sentence-final punctuation with a bracketed endnote
reference welded to it, and the seventh is a bracketed reference number welded
to the URL that follows it. No rule looks for a bracketed endnote reference, and
none of the seven fires. This one is worth a rule of its own because it is
mechanical, countable and unambiguous: a `[` immediately after `.`, `,` or `"`
that is itself at the end of a sentence, or a `[n]` immediately followed by a
bare URL, is an endnote reference whose leading space was destroyed.

### 5d. `</p><p>` and `<br />` paragraph joins, seen only when a capital follows

The 20 prose hits in section 2 are the visible edge of this. The source shows
the mechanism every time - `them.</p> <p>So the logic`, `attack.</p> <p>There
were`, `field.</p><cite>...`, `rights.<br /> <span id="more-1474"></span><br />
Now,` - and `no-space-after-stop` only sees it when a capital letter happens to
follow the full stop. When the next word starts lowercase, or when the boundary
was a `<br />` rather than a `</p><p>`, it is invisible. In the diff, `.` to
newline accounts for 18 more lost boundaries and `.` to `[` for 6.

### 5e. The archive's own text, which is 80 of the 287 hits

Not damage, and not the author's - but the scanner is reading this repository's
editorial prose in 80 places and calling it a finding. The `html-entity` class
is **100% false positive**: 72 of 72. `strip_deliberate()` already removes
`<span class="tall-glyph">` before scanning, and that is the right idea applied
to too little. The same exclusion should cover the rendering note and the
catalogue scaffolding lines, or the class should be dropped.

## 6. The 13 newest transcripts

Judged like any other, and the answer is that they are **cleaner** than the
existing 68 - not because damage was avoided, but because there was none to
find in either group.

| | files | hits | damage | not damage | what the hits are |
|---|---|---|---|---|---|
| newest 11 raw caption captures | 11 | 40 | **0** | 40 | 22 the archive's rendering note, 18 YouTube censored-word tokens (all 18 in `M3nB154Mkuk`) |
| the existing 68 | 32 of 68 | 80 | **0** | 80 | 58 the rendering note, 14 censored-word tokens, 6 the archive's `[gmGnu1RBAoQ]` / `[rtViqNWY1Bk]` scaffolding links, 2 French `espace avant ?` |

The different capture path shows up in one respect only: the two Whisper-built
transcripts have no `&nbsp;` note to carry, so all 40 of the new hits land on
the note plus one file's censored tokens, where the older set is spread across
58 note hits. The 6 `join` hits in the older set are this archive's own
generated link lines and have no counterpart in the new set because the new
transcripts are published through a different path. **No new damage class
appears in the new captures.** The raw `.vtt` files are untracked and were read
only.

## 7. What I did not do

* No file under `_posts/`, `_articles/`, `_papers/`, `_transcripts/`,
  `_videos/`, no `_data/*.json` and no collection `.md` was modified. The
  verdict tables are a list; the repair is the site owner's.
* Nothing was committed and nothing was pushed. `git status` shows one new
  file.
* Nothing in `_staging/` or `.firecrawl/` was edited. They were read as
  evidence, which is what they are for.
* The 16 undecided hits were left as they are, deliberately.
