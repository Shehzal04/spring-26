import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, url_for
from werkzeug.utils import secure_filename
import folium
import uuid
import time
import base64
from io import BytesIO
from PIL import Image
import logging

# Flask app initialize karein
app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max
app.config['SECRET_KEY'] = 'animal-detection-secret-key-2024'

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov'}

# Folders create karein
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('haarcascades', exist_ok=True)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================== MULTIPLE CASCADE CLASSIFIERS ====================
# Different cascades for better detection
cascades = {}

# 1. Face cascades (animals ke liye bhi kaam karte hain)
face_cascades = [
    ('catface', cv2.data.haarcascades + 'haarcascade_frontalcatface.xml'),
    ('catface_extended', cv2.data.haarcascades + 'haarcascade_frontalcatface_extended.xml'),
    ('frontalface', cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
    ('frontalface_alt', cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml'),
    ('frontalface_alt2', cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'),
    ('profileface', cv2.data.haarcascades + 'haarcascade_profileface.xml'),
]

# 2. Body cascades
body_cascades = [
    ('fullbody', cv2.data.haarcascades + 'haarcascade_fullbody.xml'),
    ('upperbody', cv2.data.haarcascades + 'haarcascade_upperbody.xml'),
    ('lowerbody', cv2.data.haarcascades + 'haarcascade_lowerbody.xml'),
]

# Sab cascades load karein
all_cascades = face_cascades + body_cascades

for name, path in all_cascades:
    try:
        cascade = cv2.CascadeClassifier(path)
        if not cascade.empty():
            cascades[name] = cascade
            logger.info(f"✅ Loaded cascade: {name}")
        else:
            logger.warning(f"⚠️ Empty cascade: {name}")
    except Exception as e:
        logger.error(f"❌ Failed to load {name}: {str(e)}")

logger.info(f"Total cascades loaded: {len(cascades)}")

# ==================== HELPER FUNCTIONS ====================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_image_for_detection(img):
    """Image ko enhance karein better detection ke liye"""
    try:
        # 1. Denoise
        img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        
        # 2. Increase contrast
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        lab = cv2.merge([l,a,b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return img
    except Exception as e:
        logger.error(f"Enhancement error: {str(e)}")
        return img

def detect_with_all_cascades(gray_img, color_img):
    """
    Sab cascades se detection karein
    Returns: list of detections with cascade name
    """
    all_detections = []
    detection_details = []
    
    # Image pyramids for multi-scale detection
    scales = [1.0, 0.8, 0.6]  # Different scales
    
    for scale in scales:
        if scale != 1.0:
            width = int(gray_img.shape[1] * scale)
            height = int(gray_img.shape[0] * scale)
            scaled_gray = cv2.resize(gray_img, (width, height))
            scale_factor = 1.0 / scale
        else:
            scaled_gray = gray_img
            scale_factor = 1.0
        
        # Har cascade se detection
        for name, cascade in cascades.items():
            try:
                # Different parameters for different cascade types
                if 'face' in name:
                    params = {
                        'scaleFactor': 1.05,
                        'minNeighbors': 3,
                        'minSize': (30, 30),
                        'maxSize': (300, 300)
                    }
                elif 'body' in name:
                    params = {
                        'scaleFactor': 1.1,
                        'minNeighbors': 2,
                        'minSize': (50, 50),
                        'maxSize': (500, 500)
                    }
                else:
                    params = {
                        'scaleFactor': 1.1,
                        'minNeighbors': 3,
                        'minSize': (30, 30),
                        'maxSize': (400, 400)
                    }
                
                # Detect
                detections = cascade.detectMultiScale(
                    scaled_gray,
                    scaleFactor=params['scaleFactor'],
                    minNeighbors=params['minNeighbors'],
                    minSize=params['minSize'],
                    maxSize=params['maxSize'],
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                # Scale back coordinates
                for (x, y, w, h) in detections:
                    orig_x = int(x * scale_factor)
                    orig_y = int(y * scale_factor)
                    orig_w = int(w * scale_factor)
                    orig_h = int(h * scale_factor)
                    
                    # Avoid duplicates (check if similar detection already exists)
                    is_duplicate = False
                    for existing in all_detections:
                        ex_x, ex_y, ex_w, ex_h, _ = existing
                        # Calculate overlap
                        overlap_x = max(0, min(orig_x + orig_w, ex_x + ex_w) - max(orig_x, ex_x))
                        overlap_y = max(0, min(orig_y + orig_h, ex_y + ex_h) - max(orig_y, ex_y))
                        overlap_area = overlap_x * overlap_y
                        area1 = orig_w * orig_h
                        area2 = ex_w * ex_h
                        
                        if overlap_area > 0.3 * min(area1, area2):  # 30% overlap
                            is_duplicate = True
                            break
                    
                    if not is_duplicate:
                        all_detections.append((orig_x, orig_y, orig_w, orig_h, name))
                        
                        # Color based on cascade type
                        if 'cat' in name:
                            color = (0, 255, 0)  # Green for cats
                            label = f"Cat {name}"
                        elif 'face' in name:
                            color = (255, 0, 0)  # Blue for faces
                            label = f"Face"
                        elif 'body' in name:
                            color = (0, 0, 255)  # Red for bodies
                            label = f"Body"
                        else:
                            color = (255, 255, 0)  # Yellow for others
                            label = f"Animal"
                        
                        # Draw rectangle
                        cv2.rectangle(color_img, (orig_x, orig_y), 
                                    (orig_x + orig_w, orig_y + orig_h), color, 2)
                        
                        # Add label
                        cv2.putText(color_img, label, (orig_x, orig_y - 5),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                        
                        # Store details
                        detection_details.append({
                            'cascade': name,
                            'position': [orig_x, orig_y, orig_w, orig_h],
                            'confidence': 'High' if params['minNeighbors'] <= 3 else 'Medium'
                        })
                        
            except Exception as e:
                logger.error(f"Error in cascade {name}: {str(e)}")
                continue
    
    # Remove very small detections (probably false positives)
    filtered_detections = []
    for det in all_detections:
        x, y, w, h, name = det
        if w * h > 500:  # Minimum area
            filtered_detections.append(det)
    
    return color_img, len(filtered_detections), detection_details

def detect_animals_in_image(image_path):
    """
    Main detection function
    """
    try:
        logger.info(f"Processing image: {image_path}")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            logger.error("Failed to read image")
            return None, 0, []
        
        original_img = img.copy()
        
        # Enhance image
        enhanced_img = enhance_image_for_detection(img)
        
        # Convert to grayscale
        gray = cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2GRAY)
        
        # Try with original and enhanced
        results = []
        
        # Method 1: Enhanced image
        result_img1, count1, details1 = detect_with_all_cascades(gray, enhanced_img.copy())
        
        # Method 2: Original image (if enhanced didn't work well)
        gray_original = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
        result_img2, count2, details2 = detect_with_all_cascades(gray_original, original_img.copy())
        
        # Use better result
        if count1 >= count2:
            final_img = result_img1
            final_count = count1
            final_details = details1
            logger.info(f"Using enhanced image result: {count1} detections")
        else:
            final_img = result_img2
            final_count = count2
            final_details = details2
            logger.info(f"Using original image result: {count2} detections")
        
        # Agar kuch nahi mila to try with very sensitive parameters
        if final_count == 0:
            logger.info("No detections with standard params, trying sensitive mode...")
            
            # Try with more sensitive parameters
            for name, cascade in cascades.items():
                sensitive_detections = cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.03,  # Very sensitive
                    minNeighbors=1,     # Minimum neighbors
                    minSize=(20, 20),
                    maxSize=(400, 400)
                )
                
                for (x, y, w, h) in sensitive_detections:
                    cv2.rectangle(final_img, (x, y), (x+w, y+h), (0, 255, 255), 2)
                    cv2.putText(final_img, f"Sensitive-{name}", (x, y-5),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
                    final_count += 1
                    final_details.append({
                        'cascade': f'{name}_sensitive',
                        'position': [x, y, w, h],
                        'confidence': 'Low'
                    })
        
        # Add summary text
        if final_count > 0:
            summary = f"Total Animals: {final_count}"
            if final_count == 1:
                summary += " (Single Animal)"
            elif final_count <= 3:
                summary += " (Small Herd)"
            elif final_count <= 6:
                summary += " (Medium Herd)"
            else:
                summary += " (Large Herd!)"
            
            cv2.putText(final_img, summary, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Save result
        output_filename = f"detected_{uuid.uuid4().hex}.jpg"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        cv2.imwrite(output_path, final_img)
        
        logger.info(f"Detection complete: {final_count} animals found")
        return output_path, final_count, final_details
        
    except Exception as e:
        logger.error(f"Detection error: {str(e)}")
        return None, 0, []

def create_static_map(latitude, longitude, animal_count, location_name="Unknown"):
    """
    Create a simple static map without external dependencies
    """
    try:
        # Simple HTML map using OpenStreetMap static image
        map_html = f"""
        <div style="position: relative; height: 400px; width: 100%; background: #e9ecef; border-radius: 10px; overflow: hidden;">
            <!-- Map background (OpenStreetMap static image) -->
            <img src="https://staticmap.openstreetmap.de/staticmap.php?center={latitude},{longitude}&zoom=14&size=600x400&maptype=mapnik&markers={latitude},{longitude},lightblue" 
                 style="width: 100%; height: 100%; object-fit: cover;" 
                 alt="Location Map"
                 onerror="this.onerror=null; this.src='https://via.placeholder.com/600x400?text=Map+Unavailable'">
            
            <!-- Overlay with detection info -->
            <div style="position: absolute; bottom: 20px; left: 20px; background: rgba(255,255,255,0.9); padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                <h4 style="margin: 0; color: #d9534f;">🐾 Animal Alert!</h4>
                <p style="margin: 5px 0 0 0;">
                    <strong>Location:</strong> {location_name}<br>
                    <strong>Animals:</strong> {animal_count}<br>
                    <strong>Time:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
            
            <!-- Scale bar -->
            <div style="position: absolute; bottom: 20px; right: 20px; background: rgba(0,0,0,0.7); color: white; padding: 8px 15px; border-radius: 20px; font-size: 12px;">
                <i class="fas fa-map-pin"></i> {latitude:.4f}, {longitude:.4f}
            </div>
        </div>
        """
        return map_html
        
    except Exception as e:
        logger.error(f"Map creation error: {str(e)}")
        return f"""
        <div style="padding: 30px; background: #f8d7da; border-radius: 10px; text-align: center;">
            <h4>📍 Location Information</h4>
            <p><strong>Location:</strong> {location_name}</p>
            <p><strong>Coordinates:</strong> {latitude}, {longitude}</p>
            <p><strong>Animals Detected:</strong> {animal_count}</p>
        </div>
        """

def get_default_location():
    """
    Default location return karein (Lahore)
    """
    return 31.5204, 74.3587, "Lahore, Pakistan"

# ==================== FLASK ROUTES ====================

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload and detection
    """
    try:
        # Check file
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload JPG, PNG, MP4, AVI, or MOV'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"File saved: {filepath}")
        
        # Check file size
        file_size = os.path.getsize(filepath)
        if file_size > 50 * 1024 * 1024:
            os.remove(filepath)
            return jsonify({'error': 'File too large (max 50MB)'}), 400
        
        # Process based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        
        if file_ext in ['jpg', 'jpeg', 'png']:
            # Image processing
            output_path, animal_count, details = detect_animals_in_image(filepath)
            
            if output_path is None:
                return jsonify({'error': 'Error processing image'}), 500
            
            # Get image URL
            output_filename = os.path.basename(output_path)
            image_url = url_for('static', filename=f'uploads/{output_filename}')
            
            # Get location
            lat, lon, location_name = get_default_location()
            
            # Create map
            map_html = create_static_map(lat, lon, animal_count, location_name)
            
            # Prepare response
            response = {
                'success': True,
                'message': f'✅ Detected {animal_count} animals in the image!',
                'animal_count': animal_count,
                'image_url': image_url,
                'map_html': map_html,
                'location': location_name,
                'details': details[:5]  # First 5 details only
            }
            
        elif file_ext in ['mp4', 'avi', 'mov']:
            # Video processing (simplified - first frame only)
            cap = cv2.VideoCapture(filepath)
            ret, frame = cap.read()
            cap.release()
            
            if ret:
                # Save frame
                frame_path = os.path.join(app.config['UPLOAD_FOLDER'], f"frame_{uuid.uuid4().hex}.jpg")
                cv2.imwrite(frame_path, frame)
                
                # Detect in frame
                output_path, animal_count, details = detect_animals_in_image(frame_path)
                
                if output_path:
                    image_url = url_for('static', filename=f'uploads/{os.path.basename(output_path)}')
                else:
                    image_url = None
                
                # Clean up frame
                try:
                    os.remove(frame_path)
                except:
                    pass
            else:
                image_url = None
                animal_count = 0
                details = []
            
            # Get location
            lat, lon, location_name = get_default_location()
            
            # Create map
            map_html = create_static_map(lat, lon, animal_count, location_name)
            
            response = {
                'success': True,
                'message': f'✅ Video processed! Detected {animal_count} animals in first frame.',
                'animal_count': animal_count,
                'image_url': image_url,
                'map_html': map_html,
                'location': location_name,
                'details': details[:5]
            }
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'cascades_loaded': len(cascades),
        'upload_folder': app.config['UPLOAD_FOLDER']
    })

@app.route('/debug')
def debug():
    """Debug information"""
    return jsonify({
        'cascades': list(cascades.keys()),
        'upload_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER']),
        'cascade_status': {name: not c.empty() for name, c in cascades.items()}
    })

# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🐾 ANIMAL HERD DETECTION SYSTEM - STARTING")
    print("="*60)
    
    print(f"\n📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"📊 Cascades loaded: {len(cascades)}")
    
    if len(cascades) > 0:
        print("\n✅ Active cascades:")
        for name in cascades.keys():
            print(f"   - {name}")
    else:
        print("\n❌ WARNING: No cascades loaded!")
        print("   Using fallback detection...")
    
    print(f"\n🌐 Server: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)