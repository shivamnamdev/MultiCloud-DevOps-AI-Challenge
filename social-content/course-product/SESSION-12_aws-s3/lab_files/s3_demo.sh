#!/bin/bash
# Session 12 on the emulator: boxes and labels, sync, versioning, lifecycle, policy, presign.
# Run from this folder:  export PATH="$PWD/emulator:$PATH"; ./emulator/start.sh; ./s3_demo.sh
set -u
B=atithi-photos-asha-1; mkdir -p work/photos/101 work/photos/102; cp lifecycle.json work/; cd work
aws s3 mb s3://$B
echo "room 101" > front.txt; aws s3 cp front.txt s3://$B/rooms/101/front.txt --only-show-errors
aws s3 ls s3://$B/ --recursive; aws s3 ls s3://$B/; aws s3 ls s3://$B/rooms/
echo a > photos/101/a.txt; echo b > photos/102/b.txt
aws s3 sync ./photos s3://$B/rooms/ --only-show-errors
echo "-- sync --delete, dry run first (watch what it wants to delete)"
aws s3 sync ./photos s3://$B/rooms/ --delete --dryrun
aws s3api head-object --bucket $B --key rooms/101/front.txt --query '[ContentLength,ContentType,StorageClass]' --output text
aws s3api put-public-access-block --bucket $B --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api get-public-access-block --bucket $B --query PublicAccessBlockConfiguration --output text
echo "-- versioning"
aws s3api put-bucket-versioning --bucket $B --versioning-configuration Status=Enabled
echo v1 > note.txt; aws s3 cp note.txt s3://$B/ --only-show-errors; echo v2 > note.txt; aws s3 cp note.txt s3://$B/ --only-show-errors
aws s3api list-object-versions --bucket $B --prefix note.txt --query 'Versions[].[IsLatest,Size]' --output text
aws s3 rm s3://$B/note.txt --only-show-errors; echo "after rm:"; aws s3 ls s3://$B/note.txt
aws s3api list-object-versions --bucket $B --prefix note.txt --query '{Versions:length(Versions),DeleteMarkers:length(DeleteMarkers)}' --output text
M=$(aws s3api list-object-versions --bucket $B --prefix note.txt --query 'DeleteMarkers[0].VersionId' --output text)
aws s3api delete-object --bucket $B --key note.txt --version-id $M --query DeleteMarker --output text
echo "after removing the marker:"; aws s3 ls s3://$B/note.txt; aws s3 cp s3://$B/note.txt -
echo "-- lifecycle and storage class"
aws s3api put-bucket-lifecycle-configuration --bucket $B --lifecycle-configuration file://lifecycle.json
aws s3api get-bucket-lifecycle-configuration --bucket $B --query 'Rules[0].[ID,Filter.Prefix,Transitions[0].Days,Transitions[0].StorageClass,NoncurrentVersionExpiration.NoncurrentDays]' --output text
echo cold > old.txt; aws s3 cp old.txt s3://$B/archive/old.txt --storage-class STANDARD_IA --only-show-errors
aws s3api head-object --bucket $B --key archive/old.txt --query StorageClass --output text
echo "-- presigned URL"
U=$(aws s3 presign s3://$B/rooms/101/a.txt --expires-in 300); echo "${U%%\?*}"
echo "$U" | tr '?&' '\n\n' | sed -n '2,$p' | cut -d= -f1 | tr '\n' ' '; echo
aws s3api list-object-versions --bucket $B --query '{V:length(Versions || `[]`),M:length(DeleteMarkers || `[]`)}' --output text
cp ../empty_versioned_bucket.sh . ; ./empty_versioned_bucket.sh $B; cd ..
