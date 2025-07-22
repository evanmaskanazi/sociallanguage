"""
Migration to encrypt existing sensitive data
Run this ONCE after updating the models
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from new_backend import app, db, DailyCheckin, encrypt_field

def migrate_checkin_encryption():
    """Encrypt existing checkin notes"""
    with app.app_context():
        # Get all checkins with unencrypted notes
        checkins = db.session.query(DailyCheckin).all()
        
        migrated = 0
        for checkin in checkins:
            # Check if already encrypted (will fail decryption if plain text)
            try:
                # If these fields exist and aren't encrypted yet
                if hasattr(checkin, 'emotional_notes') and checkin.emotional_notes:
                    checkin.emotional_notes_encrypted = encrypt_field(checkin.emotional_notes)
                    
                if hasattr(checkin, 'medication_notes') and checkin.medication_notes:
                    checkin.medication_notes_encrypted = encrypt_field(checkin.medication_notes)
                    
                if hasattr(checkin, 'activity_notes') and checkin.activity_notes:
                    checkin.activity_notes_encrypted = encrypt_field(checkin.activity_notes)
                    
                migrated += 1
                
            except Exception as e:
                print(f"Skipping checkin {checkin.id}: {e}")
                
        db.session.commit()
        print(f"Migrated {migrated} checkins")

if __name__ == '__main__':
    migrate_checkin_encryption()
