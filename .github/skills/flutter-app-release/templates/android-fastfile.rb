default_platform(:android)

platform :android do
  desc "Upload to internal testing track"
  lane :internal do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(
      track: "internal",
      aab: "../app/build/outputs/bundle/release/app-release.aab",
      skip_upload_apk: true
    )
  end

  desc "Promote internal to production with staged rollout"
  lane :production do
    upload_to_play_store(
      track: "internal",
      track_promote_to: "production",
      rollout: "0.1",  # 10% staged rollout
      skip_upload_aab: true,
      skip_upload_apk: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end
  
  desc "Full release to production"
  lane :release do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(
      track: "production",
      aab: "../app/build/outputs/bundle/release/app-release.aab",
      rollout: "0.1"  # Start with 10% rollout
    )
  end
  
  desc "Increase production rollout percentage"
  lane :increase_rollout do |options|
    percentage = options[:percentage] || "0.5"
    upload_to_play_store(
      track: "production",
      rollout: percentage,
      skip_upload_aab: true,
      skip_upload_apk: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end
end
