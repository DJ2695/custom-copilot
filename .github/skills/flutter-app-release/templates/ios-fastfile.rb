default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    increment_build_number(xcodeproj: "Runner.xcodeproj")
    build_app(scheme: "Runner")
    upload_to_testflight(skip_waiting_for_build_processing: true)
  end

  desc "Push a new release to the App Store"
  lane :release do
    increment_build_number(xcodeproj: "Runner.xcodeproj")
    build_app(scheme: "Runner")
    upload_to_app_store(
      force: true,
      skip_metadata: false,
      skip_screenshots: false
    )
  end
  
  desc "Take screenshots for App Store"
  lane :screenshots do
    capture_screenshots
    upload_to_app_store(
      skip_binary_upload: true,
      skip_metadata: true
    )
  end
  
  desc "Sync code signing certificates"
  lane :sync_certificates do
    match(type: "development")
    match(type: "appstore")
  end
end
