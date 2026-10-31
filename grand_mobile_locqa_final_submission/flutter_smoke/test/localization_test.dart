import 'package:flutter/widgets.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:qazaq_loc_flutter_smoke/l10n/generated/app_localizations.dart';

void main() {
  test('generated Kazakh translations preserve dynamic values', () async {
    final kk = await AppLocalizations.delegate.load(const Locale('kk'));
    expect(kk.schDuelsPointsAmount(17), contains('17'));
    expect(kk.arena_platform_colorname('КӨК'), contains('КӨК'));
    expect(kk.laBillingUnavailable('Google Play'), contains('Google Play'));
    expect(kk.userMenuReportsFromTo('Әли', 'Аян'), contains('Әли'));
    expect(kk.userMenuReportsFromTo('Әли', 'Аян'), contains('Аян'));
    expect(kk.predictionsBetsTitle, 'Бәс қабылдау');
  });
}
