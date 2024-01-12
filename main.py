#!/usr/bin/python3
import argparse
import dns.resolver
import pandas as pd

# Open the file in read mode
with open('domains.txt', 'r') as file:

    content = file.read()

    domain_list = content.split(', ')
    spf_list = []
    dmarc_list = []

for domain in domain_list:
    parser = argparse.ArgumentParser(description='Simple DMARC DKIM SPF quick test.')
    # print()
    # print ("Testing domain", domain, "for DKIM record with selector", selector, "...")
    # try:
    #   test_dkim = dns.resolver.resolve(selector + '._domainkey.' + domain , 'TXT')
    #   for dns_data in test_dkim:
    #     if 'DKIM1' in str(dns_data):
    #       print ("  [PASS] DKIM record found  :",dns_data)
    # except:
    #   print ("  [FAIL] DKIM record not found.")
    #   pass

    print()
    print ("Testing domain", domain, "for SPF record...")
    try:
      test_spf = dns.resolver.resolve(domain , 'TXT')
      for dns_data in test_spf:
        if 'spf1' in str(dns_data):
          # print ("  [PASS] SPF record found   :",dns_data)
          result_spf = f"  [PASS] SPF record found: {dns_data}"
    except:
      # print ("  [FAIL] SPF record not found.")
      result_spf = ("  [FAIL] SPF record not found.")
      pass
    
    spf_list.append(result_spf)
    print()
    print ("Testing domain", domain, "for DMARC record...")
    try:
      test_dmarc = dns.resolver.resolve('_dmarc.' + domain , 'TXT')
      for dns_data in test_dmarc:
        if 'DMARC1' in str(dns_data):
          # print ("  [PASS] DMARC record found :",dns_data)
          result_dmarc = f"  [PASS] DMARC record found: {dns_data}"
    except:
      # print ("  [FAIL] DMARC record not found.")
      result_dmarc = ("  [FAIL] DMARC record not found.")
      pass
    
    dmarc_list.append(result_dmarc)
    print ("Done")
    
data = {"Doamin name": domain_list,
        "SPF record": spf_list,
        "DMARC record": dmarc_list}

df = pd.DataFrame(data)

def highlight_cells(val):
    if 'PASS' in val:
        return 'color: green'
    elif 'FAIL' in val:
        return 'color: red'
    else:
        return ''

styled_df = df.style.applymap(highlight_cells, subset=['SPF record', 'DMARC record'])

# Save the styled DataFrame to an Excel file
styled_df.to_excel(r'export_dataframe_styled.xlsx', index=False)
