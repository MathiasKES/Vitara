document.addEventListener('DOMContentLoaded', () => {
    const typeSelect = document.getElementById('workout-type-select');
    const strengthSection = document.getElementById('strength-section');
    const exerciseRowsContainer = document.getElementById('exercise-rows');
    const addExerciseBtn = document.getElementById('add-exercise-btn');

    function toggleStrengthSection() {
        const isStrength = (typeSelect.value === 'Strength');
        strengthSection.style.display = isStrength ? 'block' : 'none';
        
        // Prevent broken required attributes passing when hidden
        const strengthInputs = strengthSection.querySelectorAll('input');
        strengthInputs.forEach(input => {
            input.disabled = !isStrength;
        });

        if (isStrength && exerciseRowsContainer.children.length === 0) {
            addExerciseRow(); // Add one row by default
        }
        
        const distanceSection = document.getElementById('distance-section');
        if (distanceSection) {
            const needsDistance = ['Running', 'Cycling', 'Swimming', 'Walking'].includes(typeSelect.value);
            distanceSection.style.display = needsDistance ? 'block' : 'none';
        }
    }

    function addExerciseRow() {
        const row = document.createElement('div');
        row.className = 'exercise-row-input';
        row.innerHTML = `
            <input type="text" name="exercise_name[]" class="form-control" placeholder="Exercise Name (e.g. Bench Press)" required>
            <input type="number" name="exercise_sets[]" class="form-control" placeholder="Sets" style="max-width: 80px;">
            <input type="number" name="exercise_reps[]" class="form-control" placeholder="Reps" style="max-width: 80px;">
            <input type="text" name="exercise_weight[]" class="form-control" placeholder="Weight (e.g. 50 or max)" style="max-width: 120px;">
            <select name="exercise_set_type[]" class="form-control" style="max-width: 110px;">
                <option value="normal">Normal</option>
                <option value="superset">Superset</option>
                <option value="dropset">Dropset</option>
            </select>
            <button type="button" class="remove-row-btn" aria-label="Remove">
                <i data-lucide="x-circle"></i>
            </button>
        `;
        exerciseRowsContainer.appendChild(row);
        
        // Re-initialize lucide icons inside the new row
        if (typeof lucide !== 'undefined') {
            lucide.createIcons();
        }

        row.querySelector('.remove-row-btn').addEventListener('click', () => {
            row.remove();
        });
    }

    if (typeSelect && strengthSection) {
        typeSelect.addEventListener('change', toggleStrengthSection);
        toggleStrengthSection(); // initial check upon load
    }

    if (addExerciseBtn) {
        addExerciseBtn.addEventListener('click', addExerciseRow);
    }
});
