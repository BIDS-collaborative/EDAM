function search_gbif(query, api_dfd, results) {
  // call gbif service
  $.ajax({
    // currently gets 5 results
    url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
    // check if there are results
    if (data.results.length != 0) {
      // extract taxonomy from first entry
      var resultObject = data.results[0];
      var taxon = [resultObject.kingdom, resultObject.phylum, resultObject.order, resultObject.family, resultObject.genus];
      var count = data.count;
      
      // update results object
      results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'count': count, 'database': 'gbif'};
    } else {
      results['gbif'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'gbif'};
    }

    // notify search complete
    api_dfd.resolve();
  });
}



var isoCountries = {
  'Canada' : 'CA',
  'Libyan Arab Jamahiriya' : 'LY',
  'Guernsey' : 'GG',
  'Saint Helena' : 'SH',
  'Lithuania' : 'LT',
  'Cambodia' : 'KH',
  'Ethiopia' : 'ET',
  'Aruba' : 'AW',
  'Swaziland' : 'SZ',
  'Belize' : 'BZ',
  'Argentina' : 'AR',
  'Bolivia' : 'BO',
  'Cameroon' : 'CM',
  'Burkina Faso' : 'BF',
  'Turkmenistan' : 'TM',
  'Ghana' : 'GH',
  'Saudi Arabia' : 'SA',
  'Togo' : 'TG',
  'Cape Verde' : 'CV',
  'Cocos (Keeling) Islands' : 'CC',
  'Faroe Islands' : 'FO',
  'Guatemala' : 'GT',
  'Kuwait' : 'KW',
  'Russian Federation' : 'RU',
  'Wallis And Futuna' : 'WF',
  'Saint Barthelemy' : 'BL',
  'Virgin Islands, British' : 'VG',
  'Spain' : 'ES',
  'Liberia' : 'LR',
  'Maldives' : 'MV',
  'Jamaica' : 'JM',
  'Iran, Islamic Republic Of' : 'IR',
  'Tanzania' : 'TZ',
  'Saint Kitts And Nevis' : 'KN',
  'Svalbard And Jan Mayen' : 'SJ',
  'Christmas Island' : 'CX',
  'Gabon' : 'GA',
  'Niue' : 'NU',
  'Monaco' : 'MC',
  'New Zealand' : 'NZ',
  'Yemen' : 'YE',
  'Jersey' : 'JE',
  'Pakistan' : 'PK',
  'Greenland' : 'GL',
  'Samoa' : 'WS',
  'Norfolk Island' : 'NF',
  'United Arab Emirates' : 'AE',
  'Guam' : 'GU',
  'Viet Nam' : 'VN',
  'Azerbaijan' : 'AZ',
  'Cote D\'Ivoire' : 'CI',
  'Lesotho' : 'LS',
  'Kenya' : 'KE',
  'Macao' : 'MO',
  'Turkey' : 'TR',
  'Afghanistan' : 'AF',
  'Northern Mariana Islands' : 'MP',
  'Andorra' : 'AD',
  'Eritrea' : 'ER',
  'Solomon Islands' : 'SB',
  'India' : 'IN',
  'Saint Lucia' : 'LC',
  'Congo, Democratic Republic' : 'CD',
  'San Marino' : 'SM',
  'French Polynesia' : 'PF',
  'France' : 'FR',
  'Syrian Arab Republic' : 'SY',
  'Bermuda' : 'BM',
  'Slovakia' : 'SK',
  'Somalia' : 'SO',
  'Peru' : 'PE',
  'Vanuatu' : 'VU',
  'Brazil' : 'BR',
  'Nauru' : 'NR',
  'Norway' : 'NO',
  'Malawi' : 'MW',
  'Cook Islands' : 'CK',
  'Benin' : 'BJ',
  'Korea' : 'KR',
  'Cuba' : 'CU',
  'Montenegro' : 'ME',
  'Djibouti' : 'DJ',
  'Heard Island & Mcdonald Islands' : 'HM',
  'British Indian Ocean Territory' : 'IO',
  'China' : 'CN',
  'Armenia' : 'AM',
  'Dominican Republic' : 'DO',
  'Germany' : 'DE',
  'Ukraine' : 'UA',
  'Bahrain' : 'BH',
  'Tonga' : 'TO',
  'Indonesia' : 'ID',
  'Qatar' : 'QA',
  'Western Sahara' : 'EH',
  'Finland' : 'FI',
  'Central African Republic' : 'CF',
  'Mauritius' : 'MU',
  'Tajikistan' : 'TJ',
  'Sweden' : 'SE',
  'Australia' : 'AU',
  'Antigua And Barbuda' : 'AG',
  'Mali' : 'ML',
  'American Samoa' : 'AS',
  'Bulgaria' : 'BG',
  'United States' : 'US',
  'Sao Tome And Principe' : 'ST',
  'Angola' : 'AO',
  'French Southern Territories' : 'TF',
  'Portugal' : 'PT',
  'South Africa' : 'ZA',
  'Tokelau' : 'TK',
  'Fiji' : 'FJ',
  'Liechtenstein' : 'LI',
  'Saint Pierre And Miquelon' : 'PM',
  'Malaysia' : 'MY',
  'Senegal' : 'SN',
  'Mozambique' : 'MZ',
  'Uganda' : 'UG',
  'Japan' : 'JP',
  'Niger' : 'NE',
  'Saint Martin' : 'MF',
  'Turks And Caicos Islands' : 'TC',
  'Pitcairn' : 'PN',
  'Guinea' : 'GN',
  'Panama' : 'PA',
  'Costa Rica' : 'CR',
  'Luxembourg' : 'LU',
  'Virgin Islands, U.S.' : 'VI',
  'Bahamas' : 'BS',
  'Gibraltar' : 'GI',
  'Ireland' : 'IE',
  'Italy' : 'IT',
  'Nigeria' : 'NG',
  'South Georgia And Sandwich Isl.' : 'GS',
  'Ecuador' : 'EC',
  'Czech Republic' : 'CZ',
  'Belarus' : 'BY',
  'Algeria' : 'DZ',
  'Slovenia' : 'SI',
  'El Salvador' : 'SV',
  'Tuvalu' : 'TV',
  'Marshall Islands' : 'MH',
  'Chile' : 'CL',
  'Puerto Rico' : 'PR',
  'Belgium' : 'BE',
  'Kiribati' : 'KI',
  'Haiti' : 'HT',
  'Iraq' : 'IQ',
  'Hong Kong' : 'HK',
  'Sierra Leone' : 'SL',
  'Georgia' : 'GE',
  'Lao People\'s Democratic Republic' : 'LA',
  'Gambia' : 'GM',
  'Poland' : 'PL',
  'Romania' : 'RO',
  'Namibia' : 'NA',
  'Moldova' : 'MD',
  'Morocco' : 'MA',
  'Albania' : 'AL',
  'Croatia' : 'HR',
  'Mongolia' : 'MN',
  'Guinea-Bissau' : 'GW',
  'Thailand' : 'TH',
  'Switzerland' : 'CH',
  'Grenada' : 'GD',
  'Bangladesh' : 'BD',
  'Honduras' : 'HN',
  'United States Outlying Islands' : 'UM',
  'Seychelles' : 'SC',
  'Chad' : 'TD',
  'Estonia' : 'EE',
  'Uruguay' : 'UY',
  'Equatorial Guinea' : 'GQ',
  'Lebanon' : 'LB',
  'Uzbekistan' : 'UZ',
  'Tunisia' : 'TN',
  'Falkland Islands (Malvinas)' : 'FK',
  'Holy See (Vatican City State)' : 'VA',
  'Timor-Leste' : 'TL',
  'Dominica' : 'DM',
  'Colombia' : 'CO',
  'Saint Vincent And Grenadines' : 'VC',
  'Burundi' : 'BI',
  'Taiwan' : 'TW',
  'Cyprus' : 'CY',
  'Reunion' : 'RE',
  'Barbados' : 'BB',
  'Madagascar' : 'MG',
  'Isle Of Man' : 'IM',
  'Palau' : 'PW',
  'Denmark' : 'DK',
  'Bhutan' : 'BT',
  'Sudan' : 'SD',
  'Nepal' : 'NP',
  'Malta' : 'MT',
  'Brunei Darussalam' : 'BN',
  'Comoros' : 'KM',
  'Netherlands' : 'NL',
  'Bosnia And Herzegovina' : 'BA',
  'Suriname' : 'SR',
  'Cayman Islands' : 'KY',
  'Anguilla' : 'AI',
  'Venezuela' : 'VE',
  'Hungary' : 'HU',
  'Aland Islands' : 'AX',
  'Israel' : 'IL',
  'Oman' : 'OM',
  'Bouvet Island' : 'BV',
  'Iceland' : 'IS',
  'Zambia' : 'ZM',
  'Austria' : 'AT',
  'Papua New Guinea' : 'PG',
  'Zimbabwe' : 'ZW',
  'Jordan' : 'JO',
  'Martinique' : 'MQ',
  'Kazakhstan' : 'KZ',
  'Philippines' : 'PH',
  'Mauritania' : 'MR',
  'Kyrgyzstan' : 'KG',
  'Mayotte' : 'YT',
  'Montserrat' : 'MS',
  'New Caledonia' : 'NC',
  'Macedonia' : 'MK',
  'Sri Lanka' : 'LK',
  'Latvia' : 'LV',
  'Guyana' : 'GY',
  'Guadeloupe' : 'GP',
  'Micronesia, Federated States Of' : 'FM',
  'Rwanda' : 'RW',
  'Myanmar' : 'MM',
  'Mexico' : 'MX',
  'Egypt' : 'EG',
  'Nicaragua' : 'NI',
  'Singapore' : 'SG',
  'Serbia' : 'RS',
  'Botswana' : 'BW',
  'United Kingdom' : 'GB',
  'Trinidad And Tobago' : 'TT',
  'Antarctica' : 'AQ',
  'Congo' : 'CG',
  'Netherlands Antilles' : 'AN',
  'Greece' : 'GR',
  'Paraguay' : 'PY',
  'French Guiana' : 'GF',
  'Palestinian Territory, Occupied' : 'PS'
};

function getCountryCode (countryName) {
    if (isoCountries.hasOwnProperty(countryName)) {
        return isoCountries[countryName];
    } else {
        return countryName;
    }
}


function search_gbif_location(query, location, api_dfd, results) {
  // call gbif service
  $.ajax({
      // currently gets 5 results
      url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
      // check if there are results
      if (data.results.length != 0) {
          // extract taxonomy and taxonKey from first entry
          var resultObject = data.results[0];
          var taxon = [resultObject.kingdom, resultObject.phylum, resultObject.order, resultObject.family, resultObject.genus];
          var taxonKey = data.results[0].taxonKey;

      }

      // get 2 letter country code
      countryCode = getCountryCode(location);

      // if country code found, search by location
      if (countryCode != location) {
        $.ajax({
            url: 'http://api.gbif.org/v1/occurrence/count?taxonKey=' + taxonKey + '&country=' + countryCode,
        }).done(function(data) {
            if (data.results.length != 0) {
              var count = data.count;
              results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'count' : count, 'database': 'gbif'};
            } else {
              results['gbif'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'gbif'};
            }
        })
      } else {
        results['gbif'] = {'name': query, 'taxonomy': 'no results', 'count': 'no results', 'database': 'gbif'};
      }

      // notify search complete
      api_dfd.resolve();
  });
}



function gbif_getCommonNameTaxonomy(query, api_dfd, results) {
  // call gbif service
  $.ajax({
      // currently gets 5 results
      url: 'http://api.gbif.org/v1/occurrence/search?scientificName=' + query + '&limit=5&offset=0',
  }).done(function(data) {
      // check if there are results
      if (data.results.length != 0) {
          // extract taxonomy and taxonKey from first entry
          var resultObject = data.results[0];
          var taxon = [resultObject.kingdom, resultObject.phylum, resultObject.order, resultObject.family, resultObject.genus];
          var taxonKey = data.results[0].taxonKey; //2435099
      }

      // search for commonNames using taxonKey
      $.ajax({
          url: 'http://api.gbif.org/v1/species/' + taxonKey +'/vernacularNames',
      }).done(function(data) {
          var commonNamesSet = new Set();
          // loop through results array an extract commonNames without repetition
          for (var i = 0; i < data.results.length; i++) {
            if (data.results[i].language == "eng") {
              commonNamesSet.add(data.results[i].vernacularName)
            }
          }
          var commonNames = Array.from(commonNamesSet);
          results['gbif'] = {'name': query, 'taxonomy': taxon.join(), 'common names' : commonNames, 'database': 'gbif'};
      });

      // notify search complete
      api_dfd.resolve();
  });
}



