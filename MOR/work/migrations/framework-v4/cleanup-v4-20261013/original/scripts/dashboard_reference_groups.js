// Presentation only. Keep original reference text, audit data and card handlers.
(() => {
  function groupReferences() {
    document.querySelectorAll('.criterionRefs > p').forEach(paragraph => {
      if (paragraph.dataset.groupedReferences) return;
      const text = paragraph.textContent;
      const marker = '; source documents: ';
      const boundary = text.indexOf(marker);
      if (boundary < 0) return;
      const crumbs = document.createElement('span');
      crumbs.className = 'referenceCrumbs';
      crumbs.style.display = 'block';
      crumbs.textContent = text.slice(0, boundary);
      const documents = document.createElement('span');
      documents.className = 'referenceDocuments';
      documents.style.display = 'block';
      const label = document.createElement('span');
      label.className = 'referenceDocumentsLabel';
      label.style.display = 'block';
      label.textContent = 'Source documents';
      documents.append(label);
      text.slice(boundary + marker.length).split(', ').forEach(name => {
        const documentName = document.createElement('span');
        documentName.className = 'referenceDocument';
        documentName.style.display = 'block';
        documentName.textContent = name;
        documents.append(documentName);
      });
      paragraph.replaceChildren(crumbs, documents);
      paragraph.dataset.groupedReferences = 'true';
    });
  }
  groupReferences();
  // Filtering/search/sorting rebuild cards. Observe only direct child changes,
  // not our own edits inside each reference paragraph.
  new MutationObserver(groupReferences).observe(document.getElementById('cards'), {childList:true});
})();
