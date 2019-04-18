import axios from 'axios';

function getCookieValue(a) {
  const b = document.cookie.match(`(^|;)\\s*${a}\\s*=\\s*([^;]+)`);
  return b ? b.pop() : '';
}

const apiPostWrapper = axios.create({
  headers: { 'X-CSRFToken': getCookieValue('csrftoken') },
});

export default {
  apiPostWrapper,
};
