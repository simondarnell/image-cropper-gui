"""
Script to help sign the executable with a certificate.

This script helps manage code signing for the ImageCropper.exe to eliminate
Windows SmartScreen warnings.

Usage:
    python sign_exe.py create_cert    # Create a self-signed certificate
    python sign_exe.py sign           # Sign the exe with certificate
    python sign_exe.py verify         # Verify the signature
"""

import subprocess
import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
EXE_PATH = PROJECT_DIR / "dist" / "ImageCropper.exe"
CERT_PATH = PROJECT_DIR / "certificate.pfx"
CERT_PASSWORD = "ImageCropper2025"


def create_self_signed_cert():
    """Create a self-signed code signing certificate."""
    print("Creating self-signed certificate...")
    print("Note: This will show security prompts on the computer")
    
    ps_script = f"""
    $cert = New-SelfSignedCertificate -DnsName "ImageCropper" `
        -Type CodeSigning `
        -CertStoreLocation Cert:\\CurrentUser\\My `
        -NotAfter (Get-Date).AddYears(5)
    
    $path = "Cert:\\CurrentUser\\My\\$($cert.Thumbprint)"
    $password = ConvertTo-SecureString -String "{CERT_PASSWORD}" -AsPlainText -Force
    
    Export-PfxCertificate -Cert $path -FilePath "{CERT_PATH}" -Password $password
    Write-Host "Certificate created: {CERT_PATH}"
    """
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("Error:", result.stderr)
            return False
        return True
    except Exception as e:
        print(f"Error creating certificate: {e}")
        return False


def sign_exe():
    """Sign the exe with the certificate."""
    if not EXE_PATH.exists():
        print(f"Error: {EXE_PATH} not found")
        print("Please build the exe first with: python build_exe_improved.py")
        return False
    
    if not CERT_PATH.exists():
        print(f"Error: {CERT_PATH} not found")
        print("Please create a certificate first with: python sign_exe.py create_cert")
        return False
    
    print(f"Signing {EXE_PATH}...")
    
    # Use signtool if available
    signtool_path = r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"
    
    if not Path(signtool_path).exists():
        print("Searching for signtool.exe...")
        # Try common locations
        for path in [
            r"C:\Program Files (x86)\Windows Kits\*\bin\*\x64\signtool.exe",
            r"C:\Program Files\Windows Kits\*\bin\*\x64\signtool.exe",
        ]:
            import glob
            matches = glob.glob(path)
            if matches:
                signtool_path = matches[0]
                break
    
    if not Path(signtool_path).exists():
        print("Error: signtool.exe not found")
        print("Please install Windows SDK:")
        print("https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/")
        return False
    
    cmd = [
        str(signtool_path),
        "sign",
        "/f", str(CERT_PATH),
        "/p", CERT_PASSWORD,
        "/t", "http://timestamp.digicert.com",
        "/fd", "sha256",
        str(EXE_PATH),
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("Error:", result.stderr)
            return False
        print("✓ Exe signed successfully!")
        return True
    except Exception as e:
        print(f"Error signing exe: {e}")
        return False


def verify_signature():
    """Verify the exe signature."""
    if not EXE_PATH.exists():
        print(f"Error: {EXE_PATH} not found")
        return False
    
    print(f"Verifying signature of {EXE_PATH}...")
    
    ps_script = f"""
    $sig = Get-AuthenticodeSignature -FilePath "{EXE_PATH}"
    Write-Host "Status: $($sig.Status)"
    Write-Host "Signer: $($sig.SignerCertificate.Subject)"
    if ($sig.Status -eq 'Valid') {{
        Write-Host "✓ Signature is valid!"
    }} else {{
        Write-Host "✗ Signature is NOT valid"
    }}
    """
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return result.returncode == 0
    except Exception as e:
        print(f"Error verifying signature: {e}")
        return False


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sign_exe.py create_cert    # Create self-signed certificate")
        print("  python sign_exe.py sign           # Sign the exe")
        print("  python sign_exe.py verify         # Verify the signature")
        return
    
    command = sys.argv[1]
    
    if command == "create_cert":
        create_self_signed_cert()
    elif command == "sign":
        sign_exe()
    elif command == "verify":
        verify_signature()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
