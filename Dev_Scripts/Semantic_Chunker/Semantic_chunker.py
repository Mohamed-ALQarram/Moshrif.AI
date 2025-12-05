import json
import time
import google.generativeai as genai
from google.api_core import retry

# 1. Setup API Key
API_KEY = "AIzaSyAumlGUx9PdwGuI7oGC10VUKof63HQz4FU" 
genai.configure(api_key=API_KEY)

# التغيير هنا: استخدمنا Pro بدلاً من Flash للدقة القصوى
# gemini-1.5-pro هو الأقوى في التحليل المنطقي والسياقي
model = genai.GenerativeModel('gemini-2.5-pro')

def get_semantic_chunks(text, video_id, max_retries=3):
    """
    Sends the transcript to Gemini Pro for high-precision semantic splitting.
    Retries up to max_retries times if JSON parsing fails.
    """
    prompt = f"""
    You are an expert linguistic analyst. 
    Analyze the following transcript from a video (ID: {video_id}) deeply.
    Your task is to perform "Semantic Chunking": split the text ONLY when the speaker drastically changes the topic.
    
    CRITICAL RULES:
    1. Accuracy is paramount. Do not split mid-thought.
    2. If the video is a Q&A, strictly separate each Question & Answer pair.
    3. If it's a lecture, separate by main chapters/concepts.
    4. Provide a descriptive title for each chunk in Arabic.
    5. Return ONLY a valid JSON array. No Markdown. No extra characters.
    
    Output Format:
    [
        {{"chunk_id": 1, "topicTitle": "وصف دقيق للموضوع", "topicContent": "Text segment..."}},
        {{"chunk_id": 2, "topicTitle": "وصف دقيق للموضوع", "topicContent": "Text segment..."}}
    ]
    
    Transcript:
    {text[:30000]} 
    """
    
    last_error = None
    last_json_text = None
    
    # Try up to max_retries times
    for attempt in range(1, max_retries + 1):
        try:
            if attempt > 1:
                print(f"  🔄 Retry attempt {attempt}/{max_retries}...")
            
            # بنعلي الـ Temperature لـ 0 عشان النتيجة تكون Deterministic ودقيقة
            response = model.generate_content(prompt, generation_config={"temperature": 0.0})
            json_text = response.text.replace("```json", "").replace("```", "").strip()
            last_json_text = json_text
            
            # Try to parse the JSON
            try:
                parsed = json.loads(json_text)
                if attempt > 1:
                    print(f"  ✅ Success on attempt {attempt}!")
                return parsed
            except json.JSONDecodeError as json_err:
                last_error = json_err
                print(f"  ⚠️ JSON Error on attempt {attempt}: {json_err}")
                
                # If this was the last attempt, save the error
                if attempt == max_retries:
                    error_file = f"failed_video_{video_id}.txt"
                    with open(error_file, "w", encoding="utf-8") as f:
                        f.write(f"Video ID: {video_id}\n")
                        f.write(f"Error: {json_err}\n")
                        f.write(f"Attempts: {max_retries}\n")
                        f.write(f"\n--- Raw Response ---\n")
                        f.write(json_text)
                    print(f"  ❌ All {max_retries} attempts failed. Saved to {error_file}")
                    
                    # Return fallback chunk
                    return [{"chunk_id": 1, "topicTitle": "فشل التحليل - Failed", "topicContent": text[:10000]}]
                # else:
                #     # Wait before retry
                #     print(f"  ⏳ Waiting 5 seconds before retry...")
                #     time.sleep(5)
                
        except Exception as e:
            last_error = e
            print(f"  ⚠️ Error on attempt {attempt}: {e}")
            
            if attempt == max_retries:
                error_file = f"failed_video_{video_id}.txt"
                with open(error_file, "w", encoding="utf-8") as f:
                    f.write(f"Video ID: {video_id}\n")
                    f.write(f"Error: {e}\n")
                    f.write(f"Attempts: {max_retries}\n")
                print(f"  ❌ All {max_retries} attempts failed. Saved to {error_file}")
                return [{"chunk_id": 1, "topicTitle": "Error Parsing", "topicContent": text[:10000]}]
            # else:
            #     time.sleep(5)
    
    # Fallback (should never reach here)
    return [{"chunk_id": 1, "topicTitle": "Error Parsing", "topicContent": text[:10000]}]

def process_large_file(input_file, output_file):
    print("🚀 Starting High-Accuracy AI Analysis (Gemini 2.5 Flash)...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    processed_data = []
    
    # Filter: Process only videos 4, 8, 15, and all from 20 onwards
    
    for i, video in enumerate(data):
        video_id = video.get('id')
        
        # Skip if not in our target list
        if video_id not in (216, 217, 218):
            print(f"[{i+1}/{len(data)}] ⏭️ Skipping Video ID: {video_id}")
            continue
            
        print(f"[{i+1}/{len(data)}] 🔄 Analyzing Video ID: {video_id}...")
        
        chunks = get_semantic_chunks(video.get('content', ''), video_id)
        
        processed_entry = {
            "id": video_id,
            "filename": video.get('filename'),
            "telegram_url": video.get('telegram_url'),
            "chunks": chunks
        }
        processed_data.append(processed_entry)
        
        # Reduced to 5 seconds for gemini-2.5-flash (faster rate limit)
        # If you get 429 errors, increase this back to 10-15 seconds
        time.sleep(15); 
        
        if (i + 1) % 2 == 0: # Save every 2 videos to be safe
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=2)
            print("💾 Progress saved.")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    print("✅ Done! Full high-accuracy processing complete.")

# Run
process_large_file(r'G:\MyProjects\Moshrif Project\Moshrif_Knowledge.json', 'Moshrif_Analyzed_ProV4.json')