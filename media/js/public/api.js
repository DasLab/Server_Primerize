if (!app.modPrimerize.errCode) {
  app.modPrimerize.errCode = {
    "00": 'Invalid primary and/or advanced options input.',
    "01": '<b>No assembly solution</b> found for sequence input under default constraints. Please supply a working assembly scheme (primers).',

    "10": 'Invalid sequence input (should be <u>at least <b>60</b> nt</u> long and without illegal characters).',
    "11": 'Sequence input exceeds length limit (should be <u>less than <b>1000</b> nt</u>). For long inputs, please download source code and run locally.',

    "20": 'Invalid advanced options input: <b>#</b> number of primers must be <b><u>EVEN</u></b>.',
    "21": 'Invalid primers input (should be in <b>pairs</b>).',

    "30": 'Invalid mutation starting and ending positions: <b>starting</b> should be <u>lower than</u> or <u>equal to</u> <b>ending</b>.',

    "40": '<b>No secondary structure</b> given for rescue design. Please supply at least one secondary structure in dot-bracket notation.',
    "41": 'Invalid structure input (<b>ALL</b> should be the same length as sequence).',

    "90": 'Required form field(s) are missing.',
    "91": 'Invalid <u>First Name</u>: only letters, numbers, and "-" allowed, and with minimum length 3 charaters required.',
    "92": 'Invalid <u>Last Name</u>: only letters, numbers, and "-" allowed, with minimum length 2 charaters required.',
    "93": 'Invalid <u>Institution</u>: only letters, numbers, and "()-, " allowed, with minimum length 3 charaters required.',
    "94": 'Invalid <u>Department</u>: only letters, numbers, and "()-, " allowed, with minimum length 3 charaters required.',
    "95": 'Invalid <u>E-mail Address</u>.'
  };
}
