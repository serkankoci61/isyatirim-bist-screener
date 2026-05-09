import pytest

from isyatirim_analiz import parse_company_page, score_company


SAMPLE_HTML = """
<html>
  <head>
    <title>BIMAS - Bim Birleşik Mağazalar A.Ş Hisse Senedi | İş Yatırım</title>
  </head>
  <body>
    <div class="stock-offer">
      <div class="top">
        <h3>Hisse Önerisi</h3>
        <div class="tip"><span class="al" id="Oneri_Aciklama">AL</span></div>
      </div>
      <div class="center">
        <ul>
          <li>Son Öneri Tarihi <span>24.04.2026</span></li>
          <li>Hedef Fiyat <span>993,77</span></li>
          <li>Getiri Pot <span>%26</span></li>
        </ul>
      </div>
    </div>

    <table>
      <tr><td>Ünvanı</td><td>Bim Birleşik Mağazalar A.Ş</td></tr>
      <tr><td>Kuruluş</td><td>31.05.1995</td></tr>
      <tr><td>Faal Alanı</td><td>Gıda ve tüketim maddeleri ticareti.</td></tr>
    </table>

    <table>
      <tr><td>F/K</td><td>25,4</td></tr>
      <tr><td>FD/FAVÖK</td><td>11,8</td></tr>
      <tr><td>PD/DD</td><td>2,9</td></tr>
      <tr><td>FD/Satışlar</td><td>0,7</td></tr>
    </table>

    <table>
      <tr><td>Satışlar</td><td>1.116.082 mn TL</td></tr>
      <tr><td>FAVÖK</td><td>75.627 mn TL</td></tr>
      <tr><td>Net Kar</td><td>28.324 mn TL</td></tr>
    </table>

    <table>
      <tr><td>Satışlar</td><td>1.046.458 mn TL</td></tr>
      <tr><td>FAVÖK</td><td>68.930 mn TL</td></tr>
      <tr><td>Net Kar</td><td>22.103 mn TL</td></tr>
    </table>

    <table>
      <tr><td>Kod</td><td>Dağ. Tarihi</td><td>Temettü Verim</td><td>Hisse Başı TL</td></tr>
      <tr><td>BIMAS</td><td>16.12.2026</td><td>0,63</td><td>5,0000</td></tr>
    </table>
  </body>
</html>
"""


def test_parse_company_page_extracts_key_isyatirim_metrics():
    snapshot = parse_company_page(SAMPLE_HTML, ticker="BIMAS")

    assert snapshot.ticker == "BIMAS"
    assert snapshot.company_name == "Bim Birleşik Mağazalar A.Ş"
    assert snapshot.recommendation == "AL"
    assert snapshot.target_price_try == pytest.approx(993.77)
    assert snapshot.upside_pct == pytest.approx(26.0)
    assert snapshot.current_pe == pytest.approx(25.4)
    assert snapshot.current_fd_favok == pytest.approx(11.8)
    assert snapshot.current_pd_dd == pytest.approx(2.9)
    assert snapshot.latest_sales_mn_try == pytest.approx(1116082.0)
    assert snapshot.previous_sales_mn_try == pytest.approx(1046458.0)
    assert snapshot.latest_net_income_mn_try == pytest.approx(28324.0)
    assert snapshot.previous_net_income_mn_try == pytest.approx(22103.0)
    assert snapshot.next_dividend_yield_pct == pytest.approx(0.63)


def test_score_company_prefers_strong_isyatirim_profile():
    snapshot = parse_company_page(SAMPLE_HTML, ticker="BIMAS")
    scored = score_company(snapshot)

    assert scored.score >= 70
    assert scored.decision == "BUY"
    assert scored.rationale
    assert "AL" in scored.rationale
