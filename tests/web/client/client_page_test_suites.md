# Manual Test Cases - Noovoleum Website Smoke Test

## Test Suite: Noovoleum Indonesia Website Smoke Test
**URL:** https://noovoleum.com/id/  
**Browser:** Chrome, Firefox, Edge  
**Test Type:** Smoke Test  
**Language:** Indonesian  

---

## TC001: Page Load and Basic Elements Verification
**Priority:** High  
**Description:** Verify that the main page loads correctly and all essential elements are present

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Wait for page to fully load (preloader should disappear)
3. Verify page title contains "noovoleum"
4. Verify main logo is displayed in header
5. Verify language toggle button shows "English"
6. Verify main heading "Making everybody a green energy champion" is visible
7. Verify Indonesian description text is displayed
8. Verify all 4 UCOllect process steps are visible with images and descriptions

### Expected Results:
- Page loads within 10 seconds
- All elements are visible and properly formatted
- No console errors
- Images load correctly

---

## TC002: Language Toggle Functionality
**Priority:** Medium  
**Description:** Verify language toggle button functionality

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Locate the "English" button in top-right corner
3. Click on the "English" button
4. Verify page redirects to English version (URL should change to https://noovoleum.com/)
5. Verify content changes to English
6. Navigate back to Indonesian version

### Expected Results:
- Language toggle button is clickable
- Page redirects to correct URL
- Content language changes appropriately
- No broken functionality after language switch

---

## TC003: Navigation and Scrolling
**Priority:** Medium  
**Description:** Verify smooth scrolling and navigation behavior

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Scroll down to view UCOllect process section
3. Continue scrolling to app download section
4. Scroll to contact form section
5. Scroll to footer section
6. Verify navbar behavior during scrolling
7. Test scroll to top functionality

### Expected Results:
- Smooth scrolling behavior
- Navbar remains fixed during scroll
- All sections load properly during scroll
- Language toggle button hides when scrolling down (after 315px)

---

## TC004: UCOllect Process Steps Verification
**Priority:** High  
**Description:** Verify all 4 UCOllect process steps are displayed correctly

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Scroll to UCOllect process section
3. Verify "UCOllect by noovoleum" logo is displayed
4. Verify Step 1: "Mengumpulkan minyak goreng bekas" with image and description
5. Verify Step 2: "Temukan tempat pengumpulan UCO terdekat" with image and description
6. Verify Step 3: "Setorkan UCO Anda ke dalam kotak pengumpulan" with image and description
7. Verify Step 4: "Dapatkan kredit instan" with image and description
8. Verify all step images load correctly
9. Verify all step descriptions are readable

### Expected Results:
- All 4 steps are visible and properly formatted
- Step images load without errors
- Text content is clear and readable
- Section layout is responsive

---

## TC005: App Download Links Verification
**Priority:** High  
**Description:** Verify mobile app download functionality

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Scroll to app download section
3. Verify "Unduh aplikasi UCOllect kami" heading is visible
4. Verify app description text is displayed
5. Verify App Store download button is present and clickable
6. Verify Google Play download button is present and clickable
7. Click on App Store button (verify it opens correct link)
8. Click on Google Play button (verify it opens correct link)
9. Verify both links point to: https://noovoleum.onelink.me/1dof/xslcyjon

### Expected Results:
- Both download buttons are visible and clickable
- Links open in new tab/window
- Links redirect to correct OneLink URL
- No broken links or 404 errors

---

## TC006: Contact Form Functionality
**Priority:** High  
**Description:** Verify contact form validation and submission

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Scroll to contact form section
3. Verify "Ayo hubungi kami" heading is visible
4. Verify form fields are present:
   - Name field (placeholder: "Your Name")
   - Email field (placeholder: "Email Address") 
   - Message field (placeholder: "Write Your Message Here")
5. Test form validation - submit empty form
6. Fill in valid data:
   - Name: "Test User"
   - Email: "test@example.com"
   - Message: "This is a test message"
7. Click "Send Message" button
8. Verify form submission behavior
9. Test invalid email format validation
10. Test required field validation

### Expected Results:
- All form fields are visible and functional
- Form validation works for required fields
- Email validation works for invalid formats
- Send button is clickable
- Appropriate feedback is shown for form submission

---

## TC007: Footer Information and Social Links
**Priority:** Medium  
**Description:** Verify footer content and social media links

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Scroll to footer section
3. Verify company logo is displayed
4. Verify Singapore address information:
   - "NOOVOLEUM PTE. LTD."
   - "3 Fraser Street #04-23A, Duo Tower, 189352 Singapore"
5. Verify Indonesia address information:
   - "PT PMA Noovoleum Indonesia Investama"
   - "Jl. Raden Patah No.6, Lebakgede, Kecamatan Coblong, Kota Bandung, Jawa Barat 40132 Indonesia"
6. Verify social media links:
   - LinkedIn: https://www.linkedin.com/company/noovoleum/
   - Instagram: https://www.instagram.com/noovoleumid/
7. Verify email link: contact@noovoleum.com
8. Test all social media links (should open in new tab)
9. Verify copyright notice: "© 2024 noovoleum. All right reserved."
10. Verify footer links: Pernyataan Diri, Pemberitahuan Privasi, Syarat dan Ketentuan

### Expected Results:
- All company information is accurate and visible
- Social media links work and open correct profiles
- Email link opens default email client
- Footer links are functional
- All text is properly formatted

---

## TC008: Responsive Design and Cross-Browser Compatibility
**Priority:** Medium  
**Description:** Verify website responsiveness and cross-browser functionality

### Test Steps:
1. Test on Chrome browser (desktop)
2. Test on Firefox browser (desktop)
3. Test on Edge browser (desktop)
4. Resize browser window to test responsive design
5. Verify mobile responsiveness (simulate mobile device)
6. Check tablet view responsiveness
7. Verify all functionality works across browsers
8. Check for any browser-specific issues

### Expected Results:
- Website functions properly on all browsers
- Responsive design adapts to different screen sizes
- No browser-specific errors or layout issues
- All interactive elements work across browsers

---

## TC009: Performance and Loading
**Priority:** Medium  
**Description:** Verify website performance and loading times

### Test Steps:
1. Navigate to https://noovoleum.com/id/
2. Monitor page load time
3. Verify preloader appears and disappears appropriately
4. Check for any slow-loading images or resources
5. Verify smooth animations and transitions
6. Test page performance on different network speeds
7. Verify no console errors during load

### Expected Results:
- Page loads within acceptable time (< 10 seconds)
- Preloader functions correctly
- All images and resources load properly
- No JavaScript errors in console
- Smooth user experience

---

## TC010: Error Handling and Edge Cases
**Priority:** Low  
**Description:** Test website behavior under edge cases

### Test Steps:
1. Test with JavaScript disabled
2. Test with images disabled
3. Test form submission with special characters
4. Test extremely long input in form fields
5. Test rapid clicking on buttons/links
6. Test browser back/forward functionality
7. Test page refresh functionality

### Expected Results:
- Website degrades gracefully when features are disabled
- Form handles edge cases appropriately
- No crashes or errors during rapid interactions
- Browser navigation works correctly