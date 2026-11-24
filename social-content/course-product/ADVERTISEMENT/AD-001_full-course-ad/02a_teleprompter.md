# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: AD-001 (Face Video)

*Extracted word-for-word from `AD-001_full-course-ad/02_script.md` ([VO] lines only). Placeholders `{{...}}` must be filled in `02_script.md` first, then this file re-extracted. Pause/slam markers are real 1-2 s pauses / a hard beat. If you edit the spoken text, edit `02_script.md` first.*

**How to use:** big font on the prompter, one beat per screen. Beat 1 is learned off-book. Each beat is recorded as its own take block, 2-3 takes each.

---


## BEAT 1: Hook

आज के टाइम पे AI एक Dockerfile, एक Kubernetes YAML और एक Jenkins pipeline लिख देता है, दस सेकंड से भी कम में। दस सेकंड।

**[PAUSE 1 s]**

तो फिर तुम DevOps क्यों सीख रहे हो? और रात के दो बजे जब production गिरेगा, तब क्या तुम्हें पता होगा कि गलती कहाँ है?


## BEAT 2: Pain mirror

तुमने Docker देखा। फिर Kubernetes। फिर Terraform, फिर Jenkins। हर हफ़्ते एक नया tool, एक नई playlist। हर वीडियो में सब समझ आया।

फिर तुमने खुद pipeline बनाई... और पहली ही run पे लाल रंग। तुमने एरर कॉपी किया, ChatGPT में paste किया, नया एरर आया, फिर paste किया।

**[LOW, CHEST VOICE]**
ये DevOps सीखना नहीं है। ये tools के नाम इकट्ठा करना है। इसी को कहते हैं tool collector बन जाना।


## BEAT 3: Fake comfort exposed

और फिर खुद को क्या दिलासा देते हो? "इतने सारे tools हैं, सब कहाँ याद रहेंगे।" "मेरा background सिस्टम वाला नहीं है।"

**[SLAM: desk tap / hard beat]**

Tools कभी प्रॉब्लम थे ही नहीं। प्रॉब्लम ये है कि तुम्हें पता ही नहीं कि ये सब आपस में जुड़ते कैसे हैं।


## BEAT 4: Wall + wrong-effort

तुम एक मोटी दीवार में सर फोड़ रहे हो और उम्मीद कर रहे हो कि दरवाज़ा खुल जाएगा। एक और certificate, एक और playlist, एक और cloud account।

पर तुम्हें ये नहीं पता कि तुम्हारा एक लाइन का code change production तक पहुँचता कैसे है। Image कहाँ बनती है? Cluster उसे कैसे उठाता है? Traffic उस तक कैसे पहुँचता है? और जब वो टूटे, तो पहला सुराग कहाँ मिलेगा? जब तक ये पूरा रास्ता नहीं पता, तुम pipeline नहीं बना रहे, YAML चिपका रहे हो।


## BEAT 5: Hope vs System

बहुत लोग महीनों से "DevOps सीख रहे हैं।" Linux का एक सीधा सवाल पूछो तो रुक जाते हैं, pipeline टूटे तो पहले ChatGPT खुलता है। क्यों? क्योंकि वो उम्मीद पर खेल रहे हैं कि "एक दिन सब अपने आप जुड़ जाएगा।" सिस्टम पर नहीं।


## BEAT 6: Thesis

**[LOW, CHEST VOICE]**
तो सुन लो। कोई जादू नहीं होने वाला। DevOps tools रटने से नहीं आता, पूरा रास्ता समझने से आता है: Build, Ship, और Fix। और ये रास्ता सिखाया जा सकता है, क्रम से, हाथ से करके, हर tool के पीछे का "क्यों" पहले और command बाद में।


## BEAT 7: Credibility

मैं Shivam Namdev हूँ। 7 साल से ज़्यादा से tech में हूँ, आज enterprise test automation और Python engineering करता हूँ, और 50 से ज़्यादा students को mentor कर चुका हूँ।

{{OPTIONAL_DEVOPS_PROOF: one true, specific sentence about your own DevOps/CI-CD work. Delete this line if none.}}

मुझे पता है कि सीखने वाला कहाँ अटकता है, और इस course का हर session उसी अटकने की जगह से शुरू होता है।


## BEAT 8: Reveal + reframe

इस course का नाम है: DevOps with AI, Build, Ship, Fix। 35 सेशन्स और एक optional bonus, 140 एपिसोड्स, करीब 35 घंटे, अपनी रफ़्तार से देखो।

AI autopilot है। Autopilot बहुत कुछ उड़ा लेता है। पर जब इंजन में आग लगती है, तो हाथ pilot का चलता है। AI तुम्हारा assistant रहेगा, pilot तुम बनोगे।


## BEAT 9: MODULE TOUR


**BLOCK 1: Foundation + AI, Sessions 1–2**

पहले नींव। Cloud और virtualization असल में क्या हैं, DevOps सच में क्या है, और AI को co-programmer की तरह कैसे इस्तेमाल करना है: उसकी हर बात पर आँख बंद करके नहीं, जाँचकर।


**BLOCK 2: Linux, Sessions 3–5**

क्योंकि production का हर server Linux पर बैठता है। Filesystem और shell से शुरू, फिर users, permissions और SSH keys, फिर storage, web server और security, और फिर वो सेशन जहाँ server बीमार पड़ता है और तुम उसे ठीक करना सीखते हो: services, networking, health-check script।


**BLOCK 3: Scripting, Sessions 6–7**

Bash और Python: वो दो औज़ार जिनसे बार-बार होने वाला काम खुद चलने लगता है।


**BLOCK 4: AWS Cloud, Sessions 8–15**

फिर Cloud, AWS पर। Server launch करना, IAM से सही इंसान को सही permission देना, storage और scaling, load balancer जो traffic बाँटता है, S3, RDS database जो मर जाए तो खुद उठ खड़ा हो। और VPC: वो networking जिससे ज़्यादातर लोग डरते हैं, यहाँ तुम खुद बनाओगे। आख़िर में CloudWatch से निगरानी और Lambda से serverless automation।


**BLOCK 5: Git + CI/CD, Sessions 16, 16B and 17–20**

अब वो हिस्सा जहाँ code production की तरफ़ चलना शुरू करता है। Git और GitHub की असली समझ और team workflows, Jenkins से पूरी pipeline, plugins और distributed builds, फिर GitHub Actions, और DevSecOps: pipeline में ही security scan, ताकि कमज़ोर image आगे जाए ही नहीं।


**BLOCK 6: Containers + Kubernetes, Sessions 21–25**

Docker: container VM से अलग क्यों है, image कैसे बनती है, Dockerfile कैसे छोटी और सुरक्षित बनती है। फिर Kubernetes: Pods, Deployments, Services, autoscaling, और GKE पर एक असली microservices app।


**BLOCK 7: Monitoring + Infrastructure as Code, Sessions 26–29**

जो दिखता नहीं, वो ठीक भी नहीं होता: Prometheus और Grafana से dashboards और alerts। और Terraform और Ansible से पूरा infrastructure कोड में: एक command, पूरा environment।


**BLOCK 8: Azure + Capstone + AI, Sessions 30–33**

Azure और Azure DevOps, ताकि तुम सिर्फ़ एक cloud के भरोसे न रहो। फिर capstone: code से production तक एक पूरी pipeline। और आख़िर में AI के साथ: cloud पर AI app और model serving, anomaly पकड़ने वाला AIOps, और अपना MCP server बनाना।

और एक optional bonus भी है: GitOps, जहाँ एक supervisor campus पर रहकर सब कुछ ठीक रखता है। ये सब एक ही कहानी है: Build, Ship, Fix। एक tool नहीं, पूरा रास्ता।


## BEAT 10: Why recorded

ये recorded course है। जहाँ अटको, वहाँ रुको, पीछे जाओ, दोबारा देखो, अपने terminal में खुद करो। कोई बैच नहीं छूटता, कोई "आज क्लास मिस हो गई" नहीं।

{{OPTIONAL_DOUBT_SUPPORT: only if real. e.g. "और हफ़्ते में दो बार live doubt session।" Delete if there is none.}}


## BEAT 11: Price reveal

अब सवाल: इसकी कीमत क्या है? मैं यहाँ कोई ऐसा course बेचने नहीं आया जो बस playlist का नया नाम हो।

{{PLAN_NAME}}: {{LAUNCH_PRICE}} रुपये [VO: {{PRICE_IN_HINDI_WORDS}}], {{GST_NOTE}}। इसमें मिलता है: 35 सेशन्स और एक optional bonus, 140 एपिसोड्स, हर एपिसोड में hands-on lab, {{ACCESS_DURATION}} की access। {{OTHER_INCLUSIONS}}

एक बात साफ़ बता दूँ: Cloud का account तुम्हारा अपना होगा, और free-tier से ऊपर चलाओगे तो उसका बिल भी तुम्हारा।

{{REFUND_POLICY_SENTENCE}}


## BEAT 12: Ultimatum + CTA

दो रास्ते हैं। या तो अगले छह महीने और tools इकट्ठा करते रहो, और रात के दो बजे फिर ChatGPT की तरफ़ देखो। या इस course से पूरा रास्ता सीखो।

AI autopilot रहेगा। Pilot तुम बनोगे। {{CTA_SPOKEN}}

**[PAUSE 2 s]**
