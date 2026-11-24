# Session 08 console demo: run sheet

You click in the AWS console. Claude checks the real state from the command line after each step (`_lab_tools/aws/demo_s8_verify.sh`, read-only) and cleans up at the end. Cost: one `t3.micro` for about 20 minutes plus an 8 GB disk, a few cents. Everything is named `atithi-demo-*` and tagged `Project = atithi-lab`, so the cleanup tool can find it.

**Before you record:** hide or blur the account number (top right menu). Do not show the downloaded `.pem` file's contents.

| # | You do in the console | Claude checks | Say or show on camera |
|---|---|---|---|
| 0 | Sign in. Top-right region selector: **Asia Pacific (Mumbai) ap-south-1**. Open **EC2**. | Nothing exists yet (baseline). | Why the region matters (script Episode 2). |
| 1 | **Launch instance**. Name: `atithi-demo-web`. Open **Add additional tags**, add `Project` = `atithi-lab`. | Nothing yet (the wizard creates things only at Launch). | What a tag is for (cost, cleanup). |
| 2 | **Application and OS Images**: choose **Ubuntu Server** (Ubuntu 24.04 LTS or the newest LTS shown). Tell Claude what is pre-selected and whether it says "Free tier eligible". | Later: the AMI id and architecture. | AMI = furnished model hotel. |
| 3 | **Instance type**: **t3.micro** (or the one marked free tier eligible). Tell Claude what it shows. | Later: the type. | Building size. |
| 4 | **Key pair**: **Create new key pair**, name `atithi-demo-key`, RSA, `.pem`. It downloads. Tell Claude where it saved. | **Key pair exists** now (the wizard creates it immediately), type `rsa`. | The only time you can download the key. |
| 5 | **Network settings**, **Edit**. Security group name `atithi-demo-sg`. Look at the default **SSH source** the wizard offers and tell Claude. Set SSH to **My IP** (not Anywhere). **Add security group rule**: HTTP, port 80, source **Anywhere**. | Later: the exact rules. | The guard at the building door. |
| 6 | **Configure storage**: leave the default. Tell Claude size and type. | Later: volume size/type, encryption, delete on termination. | |
| 7 | **Advanced details**: **Metadata version** = **V2 only (token required)**. **User data**: paste the contents of `lab_files/userdata.sh`. | Later: IMDS setting and the stored user data. | IMDSv2 and user data. |
| 8 | Read the **Summary** panel, then **Launch instance**. | Instance id, state, public IP, tags, security group rules, IMDS, user data. | The summary is the last chance to stop. |
| 9 | Wait for **Running** and **2/2 checks passed**. Open `http://PUBLIC-IP` in the browser (http, not https). | `curl` from here: page served? How many seconds after Running? | The page "Atithi Hotels: Book Now". |
| 10 | **Connect** tab: try **EC2 Instance Connect** in the browser, and SSH from your terminal with the `.pem` (`chmod 400`, `ssh -i key.pem ubuntu@PUBLIC-IP`). | SSH from here too; `cloud-init status`; IMDSv2 token test from inside. | The four SSH answers (guide D1). |
| 11 | **Stop** the instance, watch the public IP disappear; **Start**, see the new IP. | The IP before and after. | Stop is not delete. |
| 12 | **Terminate instance**. Then delete the **security group** and the **key pair** in the console, and delete the `.pem` file. | Instance `terminated`, volume gone, SG and key pair gone, leftover check clean. | Clean up the same day. |

Differences between the console and the guide are the point of this demo: tell Claude each time something looks different, and it goes into the guide.
