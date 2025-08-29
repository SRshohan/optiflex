import bcrypt
import sqlite3

def reset_user_password(user_id, email, new_password):
    # Generate proper bcrypt hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), salt)
    hashed_str = hashed.decode('utf-8')
    
    # Connect to database
    conn = sqlite3.connect('data/webui.db')
    cursor = conn.cursor()
    
    try:
        # Update password in auth table
        cursor.execute('UPDATE auth SET password = ? WHERE id = ?', (hashed_str, user_id))
        
        # Verify the update worked
        cursor.execute('SELECT password FROM auth WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        
        if result and result[0] == hashed_str:
            conn.commit()
            print(f'✅ Password successfully updated for {email}')
            print(f'New password: {new_password}')
            print(f'Hash length: {len(hashed_str)}')
            print(f'Hash starts with $2b$: {hashed_str.startswith("$2b$")}')
        else:
            print('❌ Password update failed - hash mismatch')
            
    except Exception as e:
        print(f'❌ Error: {e}')
        conn.rollback()
    finally:
        conn.close()

# Usage
user_id = '0d11d1cf-cfe6-4261-ad3d-ef59b8fdd179'
email = 'srahman06@manhattan.edu'
new_password = 'admin123'

reset_user_password(user_id, email, new_password)