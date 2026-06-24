const subjectSelect = document.getElementById('subjectInput');
const definitionInput = document.getElementById('definitionInput');
const trainingInput = document.getElementById('trainingInput');
const btnOverwriteDef = document.getElementById('btnOverwriteDef');
const btnOverwriteTrain = document.getElementById('btnOverwriteTrain');
const contentInput = document.getElementById('contentInput');
const submitButton = document.querySelector('.submit-button');
const loadingIndicator = document.getElementById('loadingIndicator');
const answerOutput = document.getElementById('answerOutput');

// Bilingual dictionary
window.i18n = {
  vi: {
    "Ask me anything about Truong Van Chien": "Hãy hỏi bất kỳ về tôi [Truong Van Chien]",
    "DEFINITION": "ĐỊNH NGHĨA",
    "Definition will be loaded from Supabase...": "Định nghĩa sẽ được tải từ Supabase...",
    "OVERWRITE DEFINITION": "GHI ĐÈ ĐỊNH NGHĨA",
    "QUESTION": "CÂU HỎI",
    "E.g., What is his current role? / What is his core tech stack? / Tell me about his Conveyor Belt 3D Printer project. / What certificates does he have?": "Ví dụ: Vai trò hiện tại của anh ấy là gì? / Các công nghệ cốt lõi anh ấy sử dụng là gì? / Hãy kể về dự án Máy in 3D băng tải của anh ấy. / Anh ấy có những chứng chỉ nào?",
    "TRAINING": "MẪU HUẤN LUYỆN",
    "Training data will be loaded from Supabase...": "Dữ liệu huấn luyện sẽ được tải từ Supabase...",
    "OVERWRITE TRAINING": "GHI ĐÈ MẪU HUẤN LUYỆN",
    "ANSWER": "CÂU TRẢ LỜI",
    "SUBMIT": "GỬI",
    // Docs
    "Asky API Documentation": "Tài liệu API Asky",
    "Integrate Asky's code analysis capabilities into your applications": "Tích hợp khả năng phân tích mã nguồn của Asky vào ứng dụng của bạn",
    "Overview": "Tổng quan",
    "Asky is a code analyst agent that uses DeepSeek LLM combined with Supabase-managed definition & training rules to predict labels and generate explanations for code snippets.": "Asky là trợ lý ảo phân tích mã nguồn hoạt động dựa trên mô hình ngôn ngữ lớn DeepSeek kết hợp với các quy tắc định nghĩa & huấn luyện được quản lý bằng cơ sở dữ liệu Supabase.",
    "Base URL": "Đường dẫn gốc (Base URL)",
    "Authentication": "Xác thực",
    "API requests are authenticated using session cookies. Ensure you authenticate by posting to the login endpoint first.": "Các yêu cầu API được xác thực bằng session cookie. Đảm bảo bạn đã đăng nhập trước khi gửi yêu cầu.",
    "Interactive Playground": "Trình chạy thử tương tác (Playground)",
    "Subject": "Chủ đề (Subject)",
    "Question": "Câu hỏi",
    "Send Request": "Gửi yêu cầu",
    "Response Preview": "Kết quả xem trước",
    "Response JSON will be displayed here...": "Kết quả phản hồi dạng JSON sẽ hiển thị tại đây...",
    // Alerts
    "alert_load_error": "Lỗi tải dữ liệu từ Supabase.",
    "alert_select_subject": "Vui lòng chọn một Subject trước.",
    "alert_overwrite_def_success": "Ghi đè Definition thành công!",
    "alert_overwrite_train_success": "Ghi đè Training thành công!",
    "alert_error_overwrite": "Lỗi khi ghi đè: ",
    "alert_empty_question": "Vui lòng nhập câu hỏi vào ô Question.",
    "alert_empty_question_docs": "Vui lòng nhập câu hỏi.",
    "prompt_password": "Vui lòng nhập mật khẩu để ghi đè:",
    "alert_wrong_password": "Mật khẩu không chính xác!"
  },
  en: {
    "Ask me anything about Truong Van Chien": "Ask me anything about Truong Van Chien",
    "DEFINITION": "DEFINITION",
    "Definition will be loaded from Supabase...": "Definition will be loaded from Supabase...",
    "OVERWRITE DEFINITION": "OVERWRITE DEFINITION",
    "QUESTION": "QUESTION",
    "E.g., What is his current role? / What is his core tech stack? / Tell me about his Conveyor Belt 3D Printer project. / What certificates does he have?": "E.g., What is his current role? / What is his core tech stack? / Tell me about his Conveyor Belt 3D Printer project. / What certificates does he have?",
    "TRAINING": "TRAINING",
    "Training data will be loaded from Supabase...": "Training data will be loaded from Supabase...",
    "OVERWRITE TRAINING": "OVERWRITE TRAINING",
    "ANSWER": "ANSWER",
    "SUBMIT": "SUBMIT",
    // Docs
    "Asky API Documentation": "Asky API Documentation",
    "Integrate Asky's code analysis capabilities into your applications": "Integrate Asky's code analysis capabilities into your applications",
    "Overview": "Overview",
    "Asky is a code analyst agent that uses DeepSeek LLM combined with Supabase-managed definition & training rules to predict labels and generate explanations for code snippets.": "Asky is a code analyst agent that uses DeepSeek LLM combined with Supabase-managed definition & training rules to predict labels and generate explanations for code snippets.",
    "Base URL": "Base URL",
    "Authentication": "Authentication",
    "API requests are authenticated using session cookies. Ensure you authenticate by posting to the login endpoint first.": "API requests are authenticated using session cookies. Ensure you authenticate by posting to the login endpoint first.",
    "Interactive Playground": "Interactive Playground",
    "Subject": "Subject",
    "Question": "Question",
    "Send Request": "Send Request",
    "Response Preview": "Response Preview",
    "Response JSON will be displayed here...": "Response JSON will be displayed here...",
    // Alerts
    "alert_load_error": "Error loading data from Supabase.",
    "alert_select_subject": "Please select a Subject first.",
    "alert_overwrite_def_success": "Overwrite Definition successful!",
    "alert_overwrite_train_success": "Overwrite Training successful!",
    "alert_error_overwrite": "Error during overwrite: ",
    "alert_connection_error": "Connection error during update.",
    "alert_empty_question": "Please enter a question in the Question box.",
    "alert_empty_question_docs": "Please enter a question.",
    "prompt_password": "Please enter the password to overwrite:",
    "alert_wrong_password": "Incorrect password!"
  }
};

window.currentLang = localStorage.getItem('lang') || 'en';

function setLanguage(lang) {
  window.currentLang = lang;
  localStorage.setItem('lang', lang);

  // Update dropdown selection
  const langSelect = document.getElementById('langSelect');
  if (langSelect) langSelect.value = lang;

  // Translate all tags with data-i18n
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (window.i18n[lang][key]) {
      el.textContent = window.i18n[lang][key];
    }
  });

  // Translate all placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (window.i18n[lang][key]) {
      el.setAttribute('placeholder', window.i18n[lang][key]);
    }
  });
}

// Bind dropdown change event
document.addEventListener('DOMContentLoaded', () => {
  const langSelect = document.getElementById('langSelect');
  if (langSelect) {
    langSelect.addEventListener('change', (e) => {
      setLanguage(e.target.value);
    });
  }
  setLanguage(window.currentLang);
});

// 1. Fetch Subject data when Subject changes or on startup
function loadSubjectData() {
  if (!subjectSelect) return;
  const subject = subjectSelect.value;
  if (!subject) return;

  // Show loading indicator
  loadingIndicator.style.display = 'block';

  fetch(`/api/chien/data?subject=${encodeURIComponent(subject)}`)
    .then((response) => response.json())
    .then((data) => {
      definitionInput.value = data.definition || '';
      trainingInput.value = data.training || '';
    })
    .catch((error) => {
      console.error('Error fetching subject data:', error);
      alert(window.i18n[window.currentLang].alert_load_error);
    })
    .finally(() => {
      loadingIndicator.style.display = 'none';
    });
}

if (subjectSelect) {
  subjectSelect.addEventListener('change', loadSubjectData);
  // Trigger data load on page startup
  loadSubjectData();
}

// 2. Overwrite Definition
if (btnOverwriteDef) {
  btnOverwriteDef.addEventListener('click', function () {
    const subject = subjectSelect.value;
    if (!subject) {
      alert(window.i18n[window.currentLang].alert_select_subject);
      return;
    }

    const pwd = prompt(window.i18n[window.currentLang].prompt_password || "Please enter the password to overwrite:");
    if (pwd !== '596512') {
      alert(window.i18n[window.currentLang].alert_wrong_password || "Incorrect password!");
      return;
    }

    const content = definitionInput.value;
    loadingIndicator.style.display = 'block';

    fetch('/api/chien/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        subject: subject,
        action: 'definition',
        content: content,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.message) {
          alert(window.i18n[window.currentLang].alert_overwrite_def_success);
        } else {
          alert(window.i18n[window.currentLang].alert_error_overwrite + (result.error || 'Unknown error'));
        }
      })
      .catch((error) => {
        console.error('Error updating definition:', error);
        alert(window.i18n[window.currentLang].alert_connection_error);
      })
      .finally(() => {
        loadingIndicator.style.display = 'none';
      });
  });
}

// 3. Overwrite Training
if (btnOverwriteTrain) {
  btnOverwriteTrain.addEventListener('click', function () {
    const subject = subjectSelect.value;
    if (!subject) {
      alert(window.i18n[window.currentLang].alert_select_subject);
      return;
    }

    const pwd = prompt(window.i18n[window.currentLang].prompt_password || "Please enter the password to overwrite:");
    if (pwd !== '596512') {
      alert(window.i18n[window.currentLang].alert_wrong_password || "Incorrect password!");
      return;
    }

    const content = trainingInput.value;
    loadingIndicator.style.display = 'block';

    fetch('/api/chien/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        subject: subject,
        action: 'training',
        content: content,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        if (result.message) {
          alert(window.i18n[window.currentLang].alert_overwrite_train_success);
        } else {
          alert(window.i18n[window.currentLang].alert_error_overwrite + (result.error || 'Unknown error'));
        }
      })
      .catch((error) => {
        console.error('Error updating training:', error);
        alert(window.i18n[window.currentLang].alert_connection_error);
      })
      .finally(() => {
        loadingIndicator.style.display = 'none';
      });
  });
}

// 4. Submit Question/Prediction to Chien
if (submitButton) {
  submitButton.addEventListener('click', function () {
    const subject = subjectSelect.value;
    if (!subject) {
      alert(window.i18n[window.currentLang].alert_select_subject);
      return;
    }

    const sample = contentInput.value.trim();
    if (!sample) {
      alert(window.i18n[window.currentLang].alert_empty_question);
      return;
    }

    const baseUrl = '/api/chien/question';
    // Show loading indicator
    loadingIndicator.style.display = 'block';
    answerOutput.textContent = '';

    fetch(baseUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content: sample, subject: subject }),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log('Result:', result);
        if (result.data && result.data.content) {
          let rawContent = result.data.content.trim();

          // Clean markdown blocks if LLM wraps JSON response inside ```json ... ```
          if (rawContent.startsWith('```json')) {
            rawContent = rawContent.replace(/^```json\s*/i, '').replace(/\s*```$/i, '').trim();
          } else if (rawContent.startsWith('```')) {
            rawContent = rawContent.replace(/^```\s*/i, '').replace(/\s*```$/i, '').trim();
          }

          try {
            const parsedJson = JSON.parse(rawContent);
            if (parsedJson && typeof parsedJson === 'object' && parsedJson.response !== undefined) {
              answerOutput.textContent = parsedJson.response;
            } else {
              answerOutput.textContent = JSON.stringify(parsedJson, null, 2);
            }
          } catch (e) {
            // Show raw string if parsing fails
            answerOutput.textContent = rawContent;
          }
        } else {
          answerOutput.textContent = 'Could not retrieve answer.';
        }
      })
      .catch((error) => {
        console.error('Error submitting question:', error);
        answerOutput.textContent = 'Error processing your request.';
      })
      .finally(() => {
        loadingIndicator.style.display = 'none';
      });
  });
}
