document.addEventListener('DOMContentLoaded', () => {
    // Hero Slider
    const slides = document.querySelectorAll('.slide');
    let currentSlide = 0;

    if (slides.length > 0) {
        setInterval(() => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }, 5000); // Change image every 5 seconds
    }

    const productGrid = document.getElementById('productGrid');

    let allProducts = [];

    function renderProducts(productsToRender) {
        productGrid.innerHTML = '';
        if (productsToRender.length === 0) {
            productGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: var(--text-muted);">Không tìm thấy sản phẩm nào trong danh mục này.</div>';
            return;
        }

        productsToRender.forEach((product, index) => {
            const link = product.link || '#';
            const card = document.createElement('a');
            card.className = 'product-card';
            card.href = link;
            card.target = '_blank';
            card.rel = 'noopener noreferrer';

            card.innerHTML = `
                <div class="product-img-wrapper">
                    <div class="product-number">${product.id}</div>
                    <img src="${product.image}" alt="${product.name}" class="product-img" loading="lazy" decoding="async" onerror="this.src='https://via.placeholder.com/400x400?text=Accnhi+Food'">
                </div>
                <div class="product-info">
                    <h3 class="product-title">${product.name}</h3>
                    <div class="btn-buy">MUA NGAY</div>
                </div>
            `;
            productGrid.appendChild(card);
        });
    }

    // Fetch the products data
    fetch('products.json')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(products => {
            allProducts = products;
            renderProducts(allProducts);
        })
        .catch(error => {
            console.error('Error fetching products:', error);
            productGrid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: red; padding: 40px;">Không thể tải danh sách sản phẩm. Vui lòng thử lại sau!</div>';
        });

    // Handle filter clicks
    const filterBtns = document.querySelectorAll('.filter-btn');
    const searchInput = document.getElementById('searchInput');

    function applyFilters() {
        const activeBtn = document.querySelector('.filter-btn.active');
        const category = activeBtn ? activeBtn.getAttribute('data-category') : 'all';
        const searchTerm = searchInput.value.toLowerCase().trim();

        let filtered = allProducts;

        // Apply Category Filter
        if (category !== 'all') {
            filtered = filtered.filter(product => {
                const name = product.name.toLowerCase();
                if (category === 'chabong') return name.includes('chà bông');
                if (category === 'dokho') return name.includes('sườn') || name.includes('khô') || name.includes('thịt băm') || name.includes('bóng cá') || name.includes('mắm') || name.includes('gà') || name.includes('bò') || name.includes('tóp mỡ');
                if (category === 'giavi') return name.includes('nước chấm') || name.includes('muối') || name.includes('bơ');
                if (category === 'anvat') return name.includes('bánh tráng') || name.includes('cơm cháy') || name.includes('rong biển') || name.includes('cốm');
                return true;
            });
        }

        // Apply Search Filter
        if (searchTerm !== '') {
            filtered = filtered.filter(product => product.name.toLowerCase().includes(searchTerm));
        }

        renderProducts(filtered);
    }

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyFilters();
        });
    });

    // Handle Search Input
    if (searchInput) {
        searchInput.addEventListener('input', applyFilters);
    }

    // Handle Suggestion Tags
    const suggestionTags = document.querySelectorAll('.suggestion-tag');
    suggestionTags.forEach(tag => {
        tag.addEventListener('click', () => {
            searchInput.value = tag.innerText;
            // Reset category to 'all' when using a suggestion to ensure global search
            filterBtns.forEach(b => b.classList.remove('active'));
            document.querySelector('.filter-btn[data-category="all"]').classList.add('active');
            applyFilters();
        });
    });
});
